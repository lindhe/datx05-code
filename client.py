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

class Client:
    def __init__(self):
        with open('/sys/class/net/lo/address') as f:
            self.hw_addr = f.read().splitlines()[0]
            if (self.hw_addr == '00:00:00:00:00:00'):
                self.hw_addr = ':'.join(['%02x']*6) % (
                            r.randint(0, 255),
                            r.randint(0, 255),
                            r.randint(0, 255),
                            r.randint(0, 255),
                            r.randint(0, 255),
                            r.randint(0, 255)
                            )

        self.loop = asyncio.get_event_loop()
        self.ec_driver = ECDriver(k=2, m=2, ec_type='liberasurecode_rs_vand')
        self.p = QuorumSend()
        t = Thread(target=self.start_event_loop, args=(self.loop, 'config/config.ini'))
        t.daemon = True
        t.start()


    def start_event_loop(self, loop, config_path):
        asyncio.set_event_loop(loop)
        config = configparser.ConfigParser()
        config.read(config_path)
        i = 0
        for key in config['Nodes']:
            ip, port = config['Nodes'][key].split(':')
            c = SenderChannel(i, 0, self.p, ip, port)
            loop.create_task(c.start())
            i = i+1
        loop.run_forever()

    def qrmAccess(self, msg):
        fut = asyncio.run_coroutine_threadsafe(self.p.phaseInit(msg), self.loop)
        return fut.result()

    def write(self, msg):
        elements = self.ec_driver.encode(msg)
        res = self.qrmAccess((None, None, 'qry', 'write'))
        max_tag = max([x.get_tag() for x in res])
        new_int = int(max_tag[0])+1
        new_tag = (new_int, self.hw_addr)
        self.qrmAccess((new_tag, elements, 'pre', 'write'))
        self.qrmAccess((new_tag, None, 'fin', 'write'))
        self.qrmAccess((new_tag, None, 'FIN', 'write'))
        print("FINISHED WRITING")

    def read(self):
        res = self.qrmAccess((None, None, 'qry', 'read'))
        max_tag = max([x.get_tag() for x in res])
        print("MAX_TAG %s" % str(max_tag))
        res = self.qrmAccess((max_tag, None, 'fin', 'read'))
        elements = [x.get_data() for x in res]
        decoded_msg = self.ec_driver.decode(elements)
        print("RESPONSE TO CLIENT %s" % str(decoded_msg))

c = Client()
time.sleep(10)
c.write(b'hello world')
c.read()
time.sleep(10)
c.write(b'(update) hello world')
c.read()
time.sleep(10)
