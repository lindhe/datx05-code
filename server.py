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

class ppAlg:
    async def callback(self):
        print("pingpong CALLBACK")
        pp_msg = PingPongMessage()
        msg = pp_msg.create_message(b'qry', b'bot',
                                    b'bot',b'none') 
        return msg
        
class GossipAlg:
    async def callback(self):
        print("Gossip CALLBACK")

p = ppAlg()
g = GossipAlg()
gossip_msg = GossipMessage()
pingTX= gossip_msg.create_message(b'tag_tuple', b'prp',
                            b'msg_all', b'echo', b'uid')

my_port = sys.argv[1]
my_ip = sys.argv[2]

loop = asyncio.get_event_loop()

config = configparser.ConfigParser()
config.read('config/config.ini')
for key in config['Nodes']:
    ip, port = config['Nodes'][key].split(':')
    if not ((ip == my_ip) and (port == my_port)):
        c = SenderChannel(1, g, ip, port, pingTX)
        loop.create_task(c.start())

s = ServerRecvChannel(p, g, my_port)
loop.create_task(s.receive())

loop.run_forever()
loop.close()
