import zmq
import zmq.asyncio
import asyncio
import configparser
import time
import threading
import math
import struct
import random as r
from threading import Thread
from channel.SenderChannel import SenderChannel
from quorum.QuorumSend import QuorumSend
from channel.ppProtocol import PingPongMessage

class Client:

    def __init__(self, cfgfile):

        self.hw_addr = self.get_hwaddr()
        self.uid = (-1, self.hw_addr)
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
        self.majority = math.ceil((nbr_of_servers+1)/2)
        self.p = QuorumSend(quorum_size, PingPongMessage)
        t = Thread(target=self.start_event_loop, args=(self.loop, config['Nodes']))
        t.daemon = True
        t.start()

    def get_hwaddr(self):
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
        return hw_addr

    def start_event_loop(self, loop, nodes):
        asyncio.set_event_loop(loop)
        i = 0
        for node in nodes:
            ip, port = nodes[node].split(':')
            c = SenderChannel(i, self.hw_addr, 0, self.p, ip, port)
            asyncio.ensure_future(c.start())
            print("Create channel to {}:{}".format(ip, port))
            i = i+1
        loop.run_forever()

    def qrmAccess(self, msg, opt_size=None):
        fut = asyncio.run_coroutine_threadsafe(self.p.phaseInit(msg, opt_size), self.loop)
        return fut.result()

    def write(self, msg):
        res = self.qrmAccess((None, None, 'qry', 'write'))
        try:
          max_tag = max([x.get_tag() for x in res])
        except Exception as e:
          print(res)
        new_int = int(max_tag[0])+1
        new_tag = (new_int, self.uid)
        self.qrmAccess((new_tag, msg, 'write', 'write'))

    def read(self):
        res = self.qrmAccess((None, None, 'qry', 'read'))
        max_tag = max([x.get_tag() for x in res])
        max_rec = [x for x in res if x.get_tag() == max_tag][0]
        self.qrmAccess((max_tag, max_rec.get_data(), 'inform', 'read'))
        return max_rec.get_data()
