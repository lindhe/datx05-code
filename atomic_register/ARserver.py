import zmq
import zmq.asyncio
import asyncio
import struct
import sys
import configparser
import math
import random as r
from channel.ppProtocol import PingPongMessage
from channel.GossipProtocol import GossipMessage
from channel.serverRecvChannel import ServerRecvChannel
from channel.SenderChannel import SenderChannel
from gossip.Gossip import Gossip
from atomic_register.QuorumRecvAR import QuorumRecvAR
from atomic_register.AtomicRegister import Server

def get_uid():
    with open('/sys/class/net/lo/address') as f:
        hw_addr = f.read().splitlines()[0]
        if (hw_addr == '00:00:00:00:00:00'):
            hw_addr = ':'.join(['%02x']*6) % (
                        r.randint(0, 255),
                        r.randint(0, 255),
                        r.randint(0, 255),
                        r.randint(0, 255),
                        r.randint(0, 255),
                        r.randint(0, 255)
                        )
    return hw_addr

def read_cfgfile(my_ip, my_port, cfgfile):
    my_addr = ":".join([my_ip, my_port])

    config = configparser.ConfigParser()
    config.read(cfgfile)
    nodes = list(config['Nodes'].values())

    my_id = 0
    for node in nodes:
        addr = node
        if (addr == my_addr):
            break
        my_id += 1

    nbr_of_servers = int(config['General']['n'])
    f = int(config['General']['f'])
    e = int(config['General']['e'])
    base_location = config['General']['storage_location']
    return [my_id, nbr_of_servers, f, e, base_location, nodes]

def start(my_ip, my_port, my_id, nbr_of_servers, f, e, base_location, nodes):
    k = nbr_of_servers - 2*(f + e)
    if(k < 1):
        raise Exception("Coded elements less than 1")
    quorum_size = math.ceil((nbr_of_servers + k + 2*e)/2)

    server = Server(my_id, quorum_size, storage_location="{}server{}/".format(base_location, my_id))
    p = QuorumRecvAR(server)

    loop = asyncio.get_event_loop()

    s = ServerRecvChannel(p, None, my_port)
    loop.create_task(s.tcp_listen())
    loop.create_task(s.udp_listen())

    loop.run_forever()
    loop.close()

def main(my_ip, my_port, cfgfile):
    parameters = read_cfgfile(my_ip, my_port, cfgfile)
    start(my_ip, my_port, *parameters)

if __name__ == '__main__':
    my_port = sys.argv[1]
    my_ip = sys.argv[2]
    cfgfile = sys.argv[3]
    main(my_ip, my_port, cfgfile)