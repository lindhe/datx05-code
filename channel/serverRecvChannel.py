import zmq
import zmq.asyncio
import asyncio
import struct
import sys
from .ppProtocol import PingPongMessage
from .GossipProtocol import GossipMessage

class ServerRecvChannel:

    def __init__(self, callback_obj_pp, callback_obj_gossip, port, gossip_freq=1):
        context = zmq.asyncio.Context()
        self.socket = context.socket(zmq.ROUTER)
        self.socket.bind("tcp://*:{}".format(port))
        self.cb_obj_pp = callback_obj_pp
        self.cb_obj_gossip = callback_obj_gossip
        self.token_size = 2*struct.calcsize("i")
        self.gsp_freq = gossip_freq
        self.tokens = {}

    async def receive(self):
        while True:
            sender, data = await self.socket.recv_multipart()
            asyncio.ensure_future(self.check_msg(data, sender))
        
    async def check_msg(self, res, sender):
        token = res[:self.token_size]
        payload = res[self.token_size:]
        msg_type, msg_cntr = struct.unpack("ii", token)
        msg = None
        
        if payload:
            if(msg_type == 0):
                msg_list = PingPongMessage.set_message(payload)
                msg = PingPongMessage(*msg_list)
            else:
                msg_list = GossipMessage.set_message(payload)
                msg = GossipMessage(*msg_list)

        if(sender not in self.tokens.keys()):
            print("Add to token list")
            self.tokens[sender] = 0

        if(self.tokens[sender] != msg_cntr):
            self.tokens[sender] = msg_cntr
            token = struct.pack("ii", msg_type,self.tokens[sender])
            if(msg_type == 0):
                if msg:
                    new_msg = await self.cb_obj_pp.arrival(msg)
                    response = token+new_msg
                else:
                    response = token
            elif(msg_type == 1):
                await self.cb_obj_gossip.arrival(sender, msg)
                response = token
                await asyncio.sleep(self.gsp_freq)
        else:
            print("NO TOKEN ARRIVAL")
            response = res

        await self.socket.send_multipart([sender, response])
