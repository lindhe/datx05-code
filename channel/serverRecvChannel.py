import zmq
import zmq.asyncio
import asyncio
import struct
import sys
from ppProtocol import PingPongMessage

class ServerRecvChannel:

    def __init__(self, callback_obj, port):
        context = zmq.asyncio.Context()
        self.socket = context.socket(zmq.ROUTER)
        self.socket.bind("tcp://*:%s" % port)
        self.cb_obj = callback_obj
        self.tokens = {}

    async def receive(self):
        while True:
            sender, data = await self.socket.recv_multipart()
            asyncio.ensure_future(self.check_msg(data, sender))
        
    async def check_msg(self, res, sender):
        int_size = struct.calcsize("i")
        msg_type, msg_cntr = struct.unpack("ii", res[:(2*int_size)])  
        print(msg_type)
        pp_msg = ""
        if(msg_type == 0):
            pp_msg = PingPongMessage()
            pp_msg.set_message(res[(2*int_size):])
        else:
            return

        if(pp_msg.get_id() not in self.tokens.keys()):
            print("Add to token list")
            self.tokens[pp_msg.get_id()] = 0

        if(self.tokens[pp_msg.get_id()] != msg_cntr): 
            new_msg = await self.cb_obj.callback()
            self.tokens[pp_msg.get_id()] = msg_cntr
            token = struct.pack("ii",0,self.tokens[pp_msg.get_id()])
            response = token+new_msg
        else:
            print("NO TOKEN ARRIVAL")
            response = res

        await asyncio.sleep(1)
        await self.socket.send_multipart([sender, response])
