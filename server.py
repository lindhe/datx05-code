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
    async def callback(self, msg_data):
        print("pingpong CALLBACK")
        if msg_data:
            print("Got message with label %s" % msg_data.get_label())
        else:
            print("Got empty message")
        pp_msg = PingPongMessage()
        msg = pp_msg.create_message(b'qry2', b'bot',
                                    b'bot',b'none') 
        return msg
        
class GossipAlgRecv:
    async def callback(self, msg_data):
        print("Gossip CALLBACK RECV")
        if msg_data:
            print("Got message with label %s" % msg_data.get_tag_tuple())
        else:
            print("Got empty message")

class GossipAlgSend:
    async def callback(self, msg_data):
        print("Gossip CALLBACK SEND")
        tag_tuple = b'tag_tuple'
        prp = b'prp'
        msg_all = b'msg_all'
        echo = b'echo'
        uid = b'uid'
        gossip_obj = GossipMessage()
        return gossip_obj.create_message(tag_tuple, prp,
                                       msg_all, echo, uid)

p = ppAlg()
gr = GossipAlgRecv()
gs = GossipAlgSend()

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
