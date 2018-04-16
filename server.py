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
from quorum.QuorumRecv import QuorumRecv
from cas.SelfStabilizing import Server

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

def main(my_ip, my_port, cfgfile):
    my_addr = ":".join([my_ip, my_port])

    config = configparser.ConfigParser()
    config.read(cfgfile)

    my_id = 0
    for node in config['Nodes']:
        addr = config['Nodes'][node]
        if (addr == my_addr):
            break
        my_id += 1

    nbr_of_servers = int(config['General']['n'])
    f = int(config['General']['f'])
    e = int(config['General']['e'])
    base_location = config['General']['storage_location']
    storage_size = int(config['General']['storage_size'])
    gossip_freq = int(config['General']['gossip_freq'])
    k = nbr_of_servers - 2*(f + e)
    if(k < 1):
        raise Exception("Coded elements less than 1")
    quorum_size = math.ceil((nbr_of_servers + k + 2*e)/2)

    server = Server(my_id, quorum_size, storage_size,  storage_location="{}server{}/".format(base_location, my_id))
    p = QuorumRecv(server)
    g = Gossip(server)

    loop = asyncio.get_event_loop()
    tag_tuple = server.get_tag_tuple()
    gossip_obj = GossipMessage(tag_tuple)
    m = gossip_obj.get_bytes()

    node_index = 0
    for node in config['Nodes']:
        ip, port = config['Nodes'][node].split(':')
        if node_index is not my_id:
            c = SenderChannel(node_index, get_uid(), 'gossip', g, ip, port, init_tx=m)
            loop.create_task(c.start())
        node_index += 1

    s = ServerRecvChannel(p, g, my_port, gossip_freq=gossip_freq)
    loop.create_task(s.tcp_listen())

    loop.run_forever()
    loop.close()

if __name__ == '__main__':
    my_port = sys.argv[1]
    my_ip = sys.argv[2]
    cfgfile = sys.argv[3]
    main(my_ip, my_port, cfgfile)
