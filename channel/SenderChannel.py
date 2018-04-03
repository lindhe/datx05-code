import zmq
import zmq.asyncio
import asyncio
import struct
import time
import socket
from .ppProtocol import PingPongMessage
from .GossipProtocol import GossipMessage

class SenderChannel:

    def __init__(self, uid, channel_type, callback_obj, ip, port, init_tx = None):
        context = zmq.asyncio.Context()
        self.uid = uid
        self.ch_type = channel_type
        self.pingTX = init_tx
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
                    if not self.ch_type:
                        msg_list = PingPongMessage.set_message(res[(2*int_size):])
                        msg_data = PingPongMessage(*msg_list)
                    else:
                        msg_list = GossipMessage.set_message(res[(2*int_size):])
                        msg_data = GossipMessage(*msg_list)
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
                self.pingTX = await self.cb_obj.departure(self.uid, msg_data)
                counter = msg_cntr+1
                token = struct.pack("ii", self.ch_type, counter)
                msg = token+self.pingTX if self.pingTX else token
                await self.socket.send_multipart([msg])
