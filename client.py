import zmq
import zmq.asyncio
import asyncio
from channel.SenderChannel import SenderChannel
from quorum.ExamplePingPongSend import ExamplePingPongSend

p = ExamplePingPongSend()
c1 = SenderChannel(0, p, "127.0.0.1", "5555")
c2 = SenderChannel(0, p, "127.0.0.1", "5556")
loop = asyncio.get_event_loop()
loop.create_task(c1.start())
loop.create_task(c2.start())
loop.run_forever()
loop.close()
