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

p = ExamplePingPongRecv()
gr = ExampleGossipRecv()
gs = ExampleGossipSend()

my_port = sys.argv[1]
my_ip = sys.argv[2]

loop = asyncio.get_event_loop()

config = configparser.ConfigParser()
config.read('config/config.ini')
for key in config['Nodes']:
    ip, port = config['Nodes'][key].split(':')
    if not ((ip == my_ip) and (port == my_port)):
        c = SenderChannel(1, gs, ip, port)
        loop.create_task(c.start())

s = ServerRecvChannel(p, gr, my_port)
loop.create_task(s.receive())

loop.run_forever()
loop.close()
