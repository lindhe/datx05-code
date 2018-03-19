import zmq
import zmq.asyncio
import asyncio
from ppProtocol import PingPongMessage
from SenderChannel import SenderChannel

class ppAlg:
    async def callback(self):
        print("pingpong arrival!")

p = ppAlg()
pp_msg = PingPongMessage()
pingTX = pp_msg.create_message(b'qry', b'bot', b'1', b'bot') 
c1 = SenderChannel(p, "127.0.0.1", "5555", pingTX)
c2 = SenderChannel(p, "127.0.0.1", "5556", pingTX)
loop = asyncio.get_event_loop()
loop.create_task(c1.start())
loop.create_task(c2.start())
loop.run_forever()
loop.close()
