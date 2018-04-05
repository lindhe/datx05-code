import zmq
import zmq.asyncio
import asyncio
import struct
import time
import socket
from .ppProtocol import PingPongMessage
from .GossipProtocol import GossipMessage

class SenderChannel:

    def __init__(self, sid, channel_type, callback_obj,
                 ip, port, timeout = 5000, init_tx = None):
        context = zmq.asyncio.Context()
        self.sid = sid
        self.ch_type = 0 if channel_type == 'pingpong' else 1
        self.tx = init_tx
        self.socket = context.socket(zmq.DEALER)
        self.socket.setsockopt(zmq.RCVTIMEO, timeout)
        self.socket.connect("tcp://{}:{}".format(ip, port))
        self.cb_obj = callback_obj
        self.token_size = 2*struct.calcsize("i")

    async def receive(self, token):
        while True:
            try:
                res = await self.socket.recv()
                token = res[:self.token_size]
                payload = res[self.token_size:]
                msg_type, msg_cntr = struct.unpack("ii", token)
                msg_data = None
                if payload:
                    if self.ch_type:
                        msg_list = GossipMessage.set_message(payload)
                        msg_data = GossipMessage(*msg_list)
                    else:
                        msg_list = PingPongMessage.set_message(payload)
                        msg_data = PingPongMessage(*msg_list)
                break
            except Exception as e:
                msg = token+self.tx if self.tx else token
                await self.socket.send_multipart([msg])
                print("TIMEOUT")
        return (msg_type, msg_cntr, msg_data)
    
    async def start(self):
        counter = 1
        while True:
            token = struct.pack("ii", self.ch_type, counter)
            msg_type, msg_cntr, msg_data = await self.receive(token)
            print("Token arrival: cntr is {}".format(msg_cntr))
            if(msg_cntr >= counter):
                self.tx = await self.cb_obj.departure(self.sid, msg_data)
                counter = msg_cntr+1
                token = struct.pack("ii", self.ch_type, counter)
                msg = token+self.tx if self.tx else token
                await self.socket.send_multipart([msg])
