import zmq
import zmq.asyncio
import asyncio
import configparser
from channel.SenderChannel import SenderChannel
from quorum.ExamplePingPongSend import ExamplePingPongSend

p = ExamplePingPongSend()

loop = asyncio.get_event_loop()

config = configparser.ConfigParser()
config.read('config/config.ini')
for key in config['Nodes']:
    ip, port = config['Nodes'][key].split(':')
    c = SenderChannel(0, p, ip, port)
    loop.create_task(c.start())

loop.run_forever()
loop.close()
