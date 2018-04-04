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

my_port = sys.argv[1]
my_ip = sys.argv[2]

config = configparser.ConfigParser()
config.read('config/config.ini')
j = 0
for key in config['Nodes']:
    ip, port = config['Nodes'][key].split(':')
    if ((ip == my_ip) and (port == my_port)):
        my_id = j
    j += 1

nbr_of_servers = int(config['General']['nodes'])
quorum_size = int(config['General']['quorumsize'])
base_location = config['General']['storage_location']

server = Server(j, quorum_size, storage_location="%sserver%s/" % (base_location, my_id))
p = QuorumRecv(server)
g = Gossip(server)

loop = asyncio.get_event_loop()
tag_tuple = server.get_tag_tuple()
gossip_obj = GossipMessage(tag_tuple)
m = gossip_obj.get_bytes()

i = 0
for key in config['Nodes']:
    ip, port = config['Nodes'][key].split(':')
    if not ((ip == my_ip) and (port == my_port)):
        c = SenderChannel(i, 'gossip', g, ip, port, init_tx=m)
        loop.create_task(c.start())
    i += 1

s = ServerRecvChannel(p, g, my_port)
loop.create_task(s.receive())

loop.run_forever()
loop.close()
