import zmq
import zmq.asyncio
import asyncio
from channel.ppProtocol import PingPongMessage
from channel.SenderChannel import SenderChannel

class ppAlg:
    async def callback(self, msg_data):
        print("pingpong arrival!")
        if msg_data:
            print("Got message with label %s" % msg_data.get_label())
        else:
            print("Got empty message")
        pp_msg = PingPongMessage()
        msg = pp_msg.create_message(b'qry', b'bot',
                                    b'bot',b'none')
        return msg

p = ppAlg()
c1 = SenderChannel(0, p, "127.0.0.1", "5555")
c2 = SenderChannel(0, p, "127.0.0.1", "5556")
loop = asyncio.get_event_loop()
loop.create_task(c1.start())
loop.create_task(c2.start())
loop.run_forever()
loop.close()
