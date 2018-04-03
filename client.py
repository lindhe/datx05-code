import zmq
import zmq.asyncio
import asyncio
import configparser
import time
import threading
import random as r
from threading import Thread
from channel.SenderChannel import SenderChannel
from quorum.QuorumSend import QuorumSend
from channel.ppProtocol import PingPongMessage

with open('/sys/class/net/lo/address') as f:
    hw_addr = f.read().splitlines()[0]
    if (hw_addr == '00:00:00:00:00:00'):
        hw_addr = ':'.join(['%02x']*6) % (
                    r.randint(0, 255),
                    r.randint(0, 255),
                    r.randint(0, 255),
                    r.randint(0, 255),
                    r.randint(0, 255),
                    r.randint(0, 255)
                    )

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

def write(msg):
    qry_msg = PingPongMessage(None, None, 'qry', 'write')
    res = qrmAccess(qry_msg, p, loop)
    max_tag = max([x.get_tag() for x in res])
    new_int = int(max_tag[0])+1
    new_tag = (new_int, hw_addr)
    pre_msg = PingPongMessage(new_tag, msg, 'pre', 'write')
    res = qrmAccess(pre_msg, p, loop)
    fin_msg = PingPongMessage(new_tag, None, 'fin', 'write')
    res = qrmAccess(fin_msg, p, loop)
    FIN_msg = PingPongMessage(new_tag, None, 'FIN', 'write')
    res = qrmAccess(FIN_msg, p, loop)
    print("FINISHED WRITING")

def read():
    qry_msg = PingPongMessage(None, None, 'qry', 'read')
    res = qrmAccess(qry_msg, p, loop)
    max_tag = max([x.get_tag() for x in res])
    print("MAX_TAG %s" % str(max_tag))
    fin_msg = PingPongMessage(max_tag, None, 'fin', 'read')
    res = qrmAccess(fin_msg, p, loop)
    elements = [x.get_data() for x in res]
    print("RESPONSE TO CLIENT %s" % str(elements))

time.sleep(10)
write(b'hello world')
read()
time.sleep(10)
write(b'(update) hello world')
read()
time.sleep(10)
