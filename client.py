import zmq
import zmq.asyncio
import asyncio
import configparser
import time
import threading
from threading import Thread
from channel.SenderChannel import SenderChannel
from quorum.QuorumSend import QuorumSend
from channel.ppProtocol import PingPongMessage

loop = asyncio.get_event_loop()
p = QuorumSend()

def start_event_loop(loop, config_path):
    asyncio.set_event_loop(loop)
    config = configparser.ConfigParser()
    config.read(config_path)
    i = 0
    for key in config['Nodes']:
        ip, port = config['Nodes'][key].split(':')
        c = SenderChannel(i, 0, p, ip, port)
        loop.create_task(c.start())
        i = i+1
    loop.run_forever()

t = Thread(target=start_event_loop, args=(loop, 'config/config.ini'))
t.daemon = True
t.start()

def qrmAccess(msg, p, loop):
    fut = asyncio.run_coroutine_threadsafe(p.phaseInit(msg), loop)
    return fut.result()

pp_msg = PingPongMessage((1,(2,3)), None, 'qry', 'read')
time.sleep(10)
res = qrmAccess(pp_msg, p, loop)
print("RESPONSE TO CLIENT %s" % res)
time.sleep(15)
