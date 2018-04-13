import asyncio
import struct
import time
import socket
from .ppProtocol import PingPongMessage
from .GossipProtocol import GossipMessage

class SenderChannel:

    def __init__(self, sid, uid, channel_type, callback_obj,
                 ip, port, timeout = 5, init_tx = None):
        self.sid = sid
        self.uid = uid.encode()
        self.ch_type = 0 if channel_type == 'pingpong' else 1
        self.tx = init_tx
        self.cb_obj = callback_obj
        self.token_size = 2*struct.calcsize("i")
        self.ip = ip
        self.port = int(port)
        self.timeout = timeout

    async def receive(self, token, loop):
        while True:
            try:
                res = await asyncio.wait_for(loop.sock_recv(self.tc_sock, 1024), self.timeout)
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
                await loop.sock_sendall(self.tc_sock, msg)
                print("TIMEOUT")
        return (msg_type, msg_cntr, msg_data)

    async def reconnect(self, loop):
        print("RECONNECT")
        self.tc_sock = socket.socket()
        self.tc_sock.setblocking(False)
        while True:
            try:
                await loop.sock_connect(self.tc_sock, (self.ip, self.port))
                print("CONNECTED")
            except OSError as e:
                print("Trying to reconnect")
                await asyncio.sleep(2)
            else:
                print("WTFI")
                break

    
    async def start(self):
        loop = asyncio.get_event_loop()
        counter = 1
        await self.reconnect(loop)
        while True:
            token = struct.pack("ii17s", self.ch_type, counter, self.uid)
            msg_type, msg_cntr, msg_data = await self.receive(token, loop)
            if __debug__:
                print("Token arrival: cntr is {}".format(msg_cntr))
            if(msg_cntr >= counter):
                self.tx = await self.cb_obj.departure(self.sid, msg_data)
                counter = msg_cntr+1
                token = struct.pack("ii17s", self.ch_type, counter, self.uid)
                msg = token+self.tx if self.tx else token
                await self.reconnect(loop)
                await loop.sock_sendall(self.tc_sock, msg)
