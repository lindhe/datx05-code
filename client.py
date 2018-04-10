import zmq
import zmq.asyncio
import asyncio
import configparser
import time
import threading
import math
import random as r
from threading import Thread
from channel.SenderChannel import SenderChannel
from quorum.QuorumSend import QuorumSend
from channel.ppProtocol import PingPongMessage
from pyeclib.ec_iface import ECDriver

class Client:

    def __init__(self, cfgfile):

        self.uid = self.get_uid()
        self.loop = asyncio.get_event_loop()
        config = configparser.ConfigParser()
        config.read(cfgfile)
        nbr_of_servers = int(config['General']['n'])
        f = int(config['General']['f'])
        e = int(config['General']['e'])
        k = nbr_of_servers - 2*(f + e)
        if(k < 1):
            raise Exception("Coded elements less than 1")
        quorum_size = math.ceil((nbr_of_servers + k + 2*e)/2)
        self.ec_driver = ECDriver(k=k, m=nbr_of_servers, ec_type='liberasurecode_rs_vand')
        self.p = QuorumSend(quorum_size)
        t = Thread(target=self.start_event_loop, args=(self.loop, config['Nodes']))
        t.daemon = True
        t.start()

    def get_uid(self):
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
        return (1, hw_addr)

    def start_event_loop(self, loop, nodes):
        asyncio.set_event_loop(loop)
        i = 0
        for node in nodes:
            ip, port = nodes[node].split(':')
            c = SenderChannel(i, 'pingpong', self.p, ip, port)
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
        new_tag = (new_int, self.uid)
        self.qrmAccess((new_tag, elements, 'pre', 'write'))
        self.qrmAccess((new_tag, None, 'fin', 'write'))
        self.qrmAccess((new_tag, None, 'FIN', 'write'))

    def read(self):
        res = self.qrmAccess((None, None, 'qry', 'read'))
        max_tag = max([x.get_tag() for x in res])
        res = self.qrmAccess((max_tag, None, 'fin', 'read'))
        elements = [x.get_data() for x in res if x.get_data()]
        try:
            decoded_msg = self.ec_driver.decode(elements)
        except:
            decoded_msg = None
        return decoded_msg
