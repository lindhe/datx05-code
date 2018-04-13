import zmq
import zmq.asyncio
import asyncio
import struct
import sys
import socket
from .ppProtocol import PingPongMessage
from .GossipProtocol import GossipMessage

class ServerRecvChannel:

    def __init__(self, callback_obj_pp, callback_obj_gossip, port, gossip_freq=1):

        self.tc_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tc_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tc_sock.setblocking(False)
        self.tc_sock.bind(('', int(port)))
        self.tc_sock.listen(10)
        self.port = port
        self.cb_obj_pp = callback_obj_pp
        self.cb_obj_gossip = callback_obj_gossip
        self.token_size = 2*struct.calcsize("i")+struct.calcsize("17s")
        self.gsp_freq = gossip_freq
        self.tokens = {}

    async def receive(self):
        loop = asyncio.get_event_loop()
        while True:
            print("Listening")
            conn, addr = await loop.sock_accept(self.tc_sock)
            print("{} got connection from {}".format(self.port, addr))
            asyncio.ensure_future(self.check_msg(conn, loop))
        
    async def check_msg(self, conn, loop):
        res = await loop.sock_recv(conn, 1024)
        token = res[:self.token_size]
        payload = res[self.token_size:]
        msg_type, msg_cntr, sender = struct.unpack("ii17s", token)
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

        await loop.sock_sendall(conn, response)
        conn.close()
        print("Connection closed")
