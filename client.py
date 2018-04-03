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
from pyeclib.ec_iface import ECDriver

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
ec_driver = ECDriver(k=2, m=2, ec_type='liberasurecode_rs_vand')
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
    elements = ec_driver.encode(msg)
    res = qrmAccess((None, None, 'qry', 'write'), p, loop)
    max_tag = max([x.get_tag() for x in res])
    new_int = int(max_tag[0])+1
    new_tag = (new_int, hw_addr)
    res = qrmAccess((new_tag, elements, 'pre', 'write'), p, loop)
    res = qrmAccess((new_tag, None, 'fin', 'write'), p, loop)
    res = qrmAccess((new_tag, None, 'FIN', 'write'), p, loop)
    print("FINISHED WRITING")

def read():
    res = qrmAccess((None, None, 'qry', 'read'), p, loop)
    max_tag = max([x.get_tag() for x in res])
    print("MAX_TAG %s" % str(max_tag))
    res = qrmAccess((max_tag, None, 'fin', 'read'), p, loop)
    elements = [x.get_data() for x in res]
    decoded_msg = ec_driver.decode(elements)
    print("RESPONSE TO CLIENT %s" % str(decoded_msg))

time.sleep(10)
write(b'hello world')
read()
time.sleep(10)
write(b'(update) hello world')
read()
time.sleep(10)
