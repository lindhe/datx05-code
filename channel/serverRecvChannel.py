import zmq
import zmq.asyncio
import asyncio
import struct
import sys
from .ppProtocol import PingPongMessage
from .GossipProtocol import GossipMessage

class ServerRecvChannel:

    def __init__(self, callback_obj_pp, callback_obj_gossip, port):
        context = zmq.asyncio.Context()
        self.socket = context.socket(zmq.ROUTER)
        self.socket.bind("tcp://*:%s" % port)
        self.cb_obj_pp = callback_obj_pp
        self.cb_obj_gossip = callback_obj_gossip
        self.tokens = {}

    async def receive(self):
        while True:
            sender, data = await self.socket.recv_multipart()
            asyncio.ensure_future(self.check_msg(data, sender))
        
    async def check_msg(self, res, sender):
        int_size = struct.calcsize("i")
        msg_type, msg_cntr = struct.unpack("ii", res[:(2*int_size)])  
        msg = None
        
        if len(res[(2*int_size):]):
            if(msg_type == 0):
                msg = PingPongMessage()
            else:
                msg = GossipMessage()

            msg.set_message(res[(2*int_size):])

        if(sender not in self.tokens.keys()):
            print("Add to token list")
            self.tokens[sender] = 0

        if(self.tokens[sender] != msg_cntr):
            self.tokens[sender] = msg_cntr
            token = struct.pack("ii",msg_type,self.tokens[sender])
            if(msg_type == 0):
                new_msg = await self.cb_obj_pp.callback(msg)
                response = token+new_msg
            elif(msg_type == 1):
                await self.cb_obj_gossip.callback(msg)
                response = token
        else:
            print("NO TOKEN ARRIVAL")
            response = res

        await asyncio.sleep(1)
        await self.socket.send_multipart([sender, response])
