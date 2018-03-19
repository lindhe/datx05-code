import zmq
import zmq.asyncio
import asyncio
import struct
import time
import socket

class ppSenderChannel:

    def __init__(self, callback_obj, ip, port, pingTX):
        context = zmq.asyncio.Context()
        self.pingTX = pingTX
        self.socket = context.socket(zmq.DEALER)
        self.socket.setsockopt(zmq.RCVTIMEO, 5000)
        self.socket.connect("tcp://%s:%s" % (ip, port))
        self.cb_obj = callback_obj

    async def receive(self, token):
        intSize = struct.calcsize("i")
        while True:
            try:
                res = await self.socket.recv()
                msg_type, msg_cntr = struct.unpack("ii", res[:(2*intSize)])  
                break
            except Exception as e:
                await self.socket.send_multipart([token+self.pingTX])
                print("TIMEOUT")
        return (msg_type, msg_cntr)
    
    async def start(self):
        counter = 1
        while True:
            token = struct.pack("ii", 0, counter)
            msg_type, msg_cntr = await self.receive(token)
            if(msg_cntr >= counter):
                await self.cb_obj.callback()
                counter = msg_cntr+1
                token = struct.pack("ii", 0, counter)
                await self.socket.send_multipart([token+self.pingTX])
            print("Client: Got response with counter %i" % msg_cntr)
