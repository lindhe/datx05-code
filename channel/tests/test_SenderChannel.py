import unittest
import struct
import mock
import asyncio
import pytest
from unittest.mock import patch
from ..ppProtocol import PingPongMessage
from ..SenderChannel import SenderChannel
from .unittest_helper import run, mock_async_method

class CallbackObj:
    async def callback(self):
        return "test"

hw_addr = "00:00:00:00:00:00"
pingpong = SenderChannel(0, hw_addr, 0, CallbackObj(), "127.0.0.1", "5555")
token = (struct.pack("ii17s", 0, 1, hw_addr.encode()), "127.0.0.1")

class TestSenderChannel(unittest.TestCase):

    @patch.object(pingpong.udp_sock, 'recvfrom', new=mock_async_method(return_value=token))
    def test_receive_no_exception(self):
        actual = run(pingpong.receive(token))
        self.assertEqual((hw_addr.encode(), 0, 1, b''), actual)
        pingpong.udp_sock.sock.close()

    @patch.object(pingpong.udp_sock, 'recvfrom', new=mock_async_method(return_value=None))
    @patch.object(pingpong.udp_sock, 'sendto', side_effect=Exception('timeout'))
    def test_receive_with_exception(self, mock_send):
        with self.assertRaises(Exception):
            run(pingpong.receive(token))
        pingpong.udp_sock.sock.close()

if __name__ == '__main__':
    unittest.main()
