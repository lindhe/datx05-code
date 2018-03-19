import zmq
import zmq.asyncio
import asyncio
import struct
import sys
from ppProtocol import PingPongMessage
from serverRecvChannel import ServerRecvChannel

class ppAlg:
    async def callback(self):
        print("CALLBACK")
        pp_msg = PingPongMessage()
        msg = pp_msg.create_message(b'qry', b'bot',
                                    b'bot',b'none') 
        return msg
        
port = sys.argv[1]
p = ppAlg()
s = ServerRecvChannel(p, port)
loop = asyncio.get_event_loop()
loop.run_until_complete(s.receive())
loop.close()
