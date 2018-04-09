import zmq
import zmq.asyncio
import asyncio
import struct
import sys
import configparser
from channel.ppProtocol import PingPongMessage
from channel.GossipProtocol import GossipMessage
from channel.serverRecvChannel import ServerRecvChannel
from channel.SenderChannel import SenderChannel
from gossip.Gossip import Gossip
from quorum.QuorumRecv import QuorumRecv
from cas.SelfStabilizing import Server

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

    nbr_of_servers = int(config['General']['nodes'])
    quorum_size = int(config['General']['quorumsize'])
    base_location = config['General']['storage_location']
    storage_size = int(config['General']['storage_size'])

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
            c = SenderChannel(node_index, 'gossip', g, ip, port, init_tx=m)
            loop.create_task(c.start())
        node_index += 1

    s = ServerRecvChannel(p, g, my_port)
    loop.create_task(s.receive())

    loop.run_forever()
    loop.close()

if __name__ == '__main__':
    my_port = sys.argv[1]
    my_ip = sys.argv[2]
    cfgfile = sys.argv[3]
    main(my_ip, my_port, cfgfile)
