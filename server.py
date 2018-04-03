import zmq
import zmq.asyncio
import asyncio
import struct
import sys
import configparser
from channel.ppProtocol import PingPongMessage
from channel.serverRecvChannel import ServerRecvChannel
from channel.SenderChannel import SenderChannel
from gossip.ExampleGossipRecv import ExampleGossipRecv
from gossip.ExampleGossipSend import ExampleGossipSend
from quorum.ExamplePingPongRecv import ExamplePingPongRecv
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

server = Server(j, 3)
p = QuorumRecv(server)
gr = ExampleGossipRecv()
gs = ExampleGossipSend()

loop = asyncio.get_event_loop()

i = 0
for key in config['Nodes']:
    ip, port = config['Nodes'][key].split(':')
    if not ((ip == my_ip) and (port == my_port)):
        c = SenderChannel(i, 1, gs, ip, port)
        loop.create_task(c.start())

s = ServerRecvChannel(p, gr, my_port)
loop.create_task(s.receive())

loop.run_forever()
loop.close()
