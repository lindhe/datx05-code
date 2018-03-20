import zmq
import zmq.asyncio
import asyncio
import struct
import sys
from ppProtocol import PingPongMessage
from GossipProtocol import GossipMessage
from serverRecvChannel import ServerRecvChannel
from SenderChannel import SenderChannel

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
        gossip_msg = GossipMessage()
        msg = gossip_msg.create_message(b'tag_tuple', b'prp',
                                    b'msg_all', b'echo', b'uid')
        return msg

port = sys.argv[1]
p = ppAlg()
g = GossipAlg()
gossip_msg = GossipMessage()
pingTX= gossip_msg.create_message(b'tag_tuple', b'prp',
                            b'msg_all', b'echo', b'uid')
if(port == "5556"):
    c1 = SenderChannel(1, g, "127.0.0.1", "5555", pingTX)
else:
    c1 = SenderChannel(1, g, "127.0.0.1", "5556", pingTX)
s = ServerRecvChannel(p, g, port)
loop = asyncio.get_event_loop()
loop.create_task(c1.start())
loop.create_task(s.receive())
loop.run_forever()
loop.close()
