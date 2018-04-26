import asyncio
import struct
import socket
import io
from .ppProtocol import PingPongMessage
from .GossipProtocol import GossipMessage
from .UdpSender import UdpSender

class ServerRecvChannel:
    """ Creates a server recv channel for pingpong and gossip"""

    def __init__(self, uid, callback_obj_pp, callback_obj_gossip, port,
                 gossip_freq=1, chunks_size=1024):
        """
        Initialize callbacks, parameters and create tcp/udp sockets
        """

        self.uid = uid.encode()
        self.cb_obj_pp = callback_obj_pp
        self.cb_obj_gossip = callback_obj_gossip
        self.port = port
        self.gsp_freq = gossip_freq
        self.chunks_size = chunks_size

        self.loop = asyncio.get_event_loop()
        self.udp_sock = UdpSender(self.loop, '', int(port))
        self.token_size = 2*struct.calcsize("i")+struct.calcsize("17s")
        self.tokens = {}

        self.tc_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tc_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tc_sock.setblocking(False)
        self.tc_sock.bind(('', int(port)))
        self.tc_sock.listen(10)

    async def tcp_listen(self):
        """
        Wait for tcp connections to arrive
        """
        while True:
            print("Listening")
            conn, addr = await self.loop.sock_accept(self.tc_sock)
            print("{} got tcp connection from {}".format(self.port, addr))
            asyncio.ensure_future(self.tcp_response(conn))

    async def udp_listen(self):
        """
        Wait until udp message arrives.
        """
        while True:
            print("Listening")
            data, addr = await self.udp_sock.recvfrom(self.chunks_size)
            print("{} got udp request from {}".format(self.port, addr))
            asyncio.ensure_future(self.udp_response(data, addr))

    async def udp_response(self, data, addr):
        """
        Create udp response and send it.
        """
        response = await self.check_msg(data)
        await self.udp_sock.sendto(response, addr)

    async def tcp_response(self, conn):
        """
        Receive tcp stream, create response and send it
        """
        int_size = struct.calcsize("i")
        recv_msg_size = await self.loop.sock_recv(conn, int_size)
        msg_size = struct.unpack("i", recv_msg_size)[0]
        res = b''
        while (len(res) < msg_size):
            res += await self.loop.sock_recv(conn, self.chunks_size)
            await asyncio.sleep(0)
        response = await self.check_msg(res)
        response_stream = io.BytesIO(response)
        stream = True
        while stream:
            stream = response_stream.read(self.chunks_size)
            await self.loop.sock_sendall(conn, stream)
        conn.close()
        print("Connection closed")
        
    async def check_msg(self, res):
        """
        Determine message type and create response message accordingly
        """
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
            token = struct.pack("ii17s", msg_type,self.tokens[sender], self.uid)
            if(msg_type == 0):
                if msg:
                    new_msg = await self.cb_obj_pp.arrival(sender, msg)
                    response = token+new_msg if new_msg else token
                else:
                    response = token
            elif(msg_type == 1):
                await self.cb_obj_gossip.arrival(sender, msg)
                response = token
                await asyncio.sleep(self.gsp_freq)
        else:
            print("NO TOKEN ARRIVAL")
            token = struct.pack("ii17s", msg_type,self.tokens[sender], self.uid)
            response = token

        return response
