import asyncio
import socket
'''
recvfrom and sendto are taken from:
https://github.com/crazyguitar/pysheeet/blob/master/docs/notes/python-asyncio.rst#simple-asyncio-udp-echo-server
under MIT license
'''
class UdpSender:

    def __init__(self, loop, ip, port):
        self.loop = loop
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setblocking(False)
        self.sock = sock
        self.sock.bind((ip, port))

    def recvfrom(self, n_bytes, fut=None, registed=False):
        fd = self.sock.fileno()
        if fut is None:
            fut = self.loop.create_future()
        if registed:
            self.loop.remove_reader(fd)

        try:
            data, addr = self.sock.recvfrom(n_bytes)
        except (BlockingIOError, InterruptedError):
            self.loop.add_reader(fd, self.recvfrom, n_bytes, fut, True)
        else:
            fut.set_result((data, addr))
        return fut

    def sendto(self, data, addr, fut=None, registed=False):
        fd = self.sock.fileno()
        if fut is None:
            fut = self.loop.create_future()
        if registed:
            self.loop.remove_writer(fd)
        if not data:
            return

        try:
            n = self.sock.sendto(data, addr)
        except (BlockingIOError, InterruptedError):
            self.loop.add_writer(fd, self.sendto, data, addr, fut, True)
        else:
            fut.set_result(n)
        return fut
