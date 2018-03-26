import zmq
import zmq.asyncio
import asyncio
import struct
import time
import socket
from .ppProtocol import PingPongMessage
from .GossipProtocol import GossipMessage

class SenderChannel:

    def __init__(self, channel_type, callback_obj, ip, port):
        context = zmq.asyncio.Context()
        self.ch_type = channel_type
        self.pingTX = None
        if channel_type:
            self.msg_obj = GossipMessage()
        else:
            self.msg_obj = PingPongMessage()
        self.socket = context.socket(zmq.DEALER)
        self.socket.setsockopt(zmq.RCVTIMEO, 5000)
        self.socket.connect("tcp://%s:%s" % (ip, port))
        self.cb_obj = callback_obj

    async def receive(self, token):
        int_size = struct.calcsize("i")
        while True:
            try:
                res = await self.socket.recv()
                msg_type, msg_cntr = struct.unpack("ii", res[:(2*int_size)])  
                msg_data = None
                if len(res[(2*int_size):]):
                    self.msg_obj.set_message(res[(2*int_size):])
                    msg_data = self.msg_obj
                break
            except Exception as e:
                msg = token+self.pingTX if self.pingTX else token
                await self.socket.send_multipart([msg])
                print("TIMEOUT")
        return (msg_type, msg_cntr, msg_data)
    
    async def start(self):
        counter = 1
        while True:
            token = struct.pack("ii", self.ch_type, counter)
            msg_type, msg_cntr, msg_data = await self.receive(token)
            print("Got response with counter %i" % msg_cntr)
            if(msg_cntr >= counter):
                self.pingTX = await self.cb_obj.departure(msg_data)
                counter = msg_cntr+1
                token = struct.pack("ii", self.ch_type, counter)
                msg = token+self.pingTX if self.pingTX else token
                await self.socket.send_multipart([msg])
