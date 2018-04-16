import asyncio
import struct
import time
import socket
import io
from .ppProtocol import PingPongMessage
from .GossipProtocol import GossipMessage
from .UdpSender import UdpSender

class SenderChannel:

    def __init__(self, sid, uid, channel_type, callback_obj,
                 ip, port, timeout = 5, init_tx = None):
        self.loop = asyncio.get_event_loop()
        self.sid = sid
        self.uid = uid.encode()
        self.ch_type = 0 if channel_type == 'pingpong' else 1
        self.tx = init_tx
        self.udp = True
        self.cb_obj = callback_obj
        self.token_size = 2*struct.calcsize("i")
        self.ip = ip
        self.port = int(port)
        self.addr  = (ip, int(port))
        self.timeout = timeout
        self.udp_sock = UdpSender(self.loop)

    async def receive(self, token):
        while True:
            try:
                if self.udp:
                    res, addr = await asyncio.wait_for(self.udp_sock.recvfrom(1024), self.timeout)
                else:
                    res = b''
                    while True:
                        res_part = await asyncio.wait_for(self.loop.sock_recv(self.tc_sock, 1024), self.timeout)
                        if not res_part:
                            break
                        else:
                            res += res_part
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
                print(e)
                if self.udp:
                    print("Sending udp to %s" % str(self.addr))
                    await self.udp_sock.sendto(msg, self.addr)
                else:
                    await self.reconnect()
                    await self.tcp_send(self.tc_sock, msg)
                print("TIMEOUT")
        return (msg_type, msg_cntr, msg_data)

    async def reconnect(self):
        self.tc_sock = socket.socket()
        self.tc_sock.setblocking(False)
        while True:
            try:
                await self.loop.sock_connect(self.tc_sock, (self.ip, self.port))
            except OSError as e:
                print("Trying to reconnect")
                await asyncio.sleep(2)
            else:
                break
    
    async def start(self):
        counter = 1
        while True:
            token = struct.pack("ii17s", self.ch_type, counter, self.uid)
            msg_type, msg_cntr, msg_data = await self.receive(token)
            if __debug__:
                print("Token arrival: cntr is {}".format(msg_cntr))
            if(msg_cntr >= counter):
                self.tx, self.udp = await self.cb_obj.departure(self.sid, msg_data)
                counter = msg_cntr+1
                token = struct.pack("ii17s", self.ch_type, counter, self.uid)
                msg = token+self.tx if self.tx else token
                if self.udp:
                    await self.udp_sock.sendto(msg, self.addr)
                else:
                    await self.reconnect()
                    await self.tcp_send(self.tc_sock, msg)
 
    async def tcp_send(self, conn, msg):
        msg_size = struct.pack("i", len(msg))
        response_stream = io.BytesIO(msg_size+msg)
        stream = True
        while stream:
            stream = response_stream.read(1024)
            await self.loop.sock_sendall(conn, stream)
