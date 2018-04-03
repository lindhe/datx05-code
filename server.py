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

server = Server(j, 3, storage_location="./.storage/server%s/"%my_id)
p = QuorumRecv(server)
g = Gossip(server)

loop = asyncio.get_event_loop()
tag_tuple = server.get_tag_tuple()
prp = (1,None)
msg_all = False
echo = (prp, msg_all)
gossip_obj = GossipMessage(tag_tuple, prp, msg_all, echo)
m = gossip_obj.get_bytes()

i = 0
for key in config['Nodes']:
    ip, port = config['Nodes'][key].split(':')
    if not ((ip == my_ip) and (port == my_port)):
        c = SenderChannel(i, 1, g, ip, port, init_tx=m)
        #loop.create_task(c.start())
    i += 1

s = ServerRecvChannel(p, g, my_port)
loop.create_task(s.receive())

loop.run_forever()
loop.close()
