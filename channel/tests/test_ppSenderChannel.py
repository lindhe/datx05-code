import unittest
import struct
import mock
from unittest.mock import patch
from ppProtocol import PingPongMessage
from ppSenderChannel import ppSenderChannel
from .unittest_helper import run, mock_async_method
import zmq
import asyncio
import pytest

class CallbackObj:
    async def callback(self):
        return "test"

pingpong = ppSenderChannel(CallbackObj(), "127.0.0.1", "5555", b'0')
token = struct.pack("ii", 0, 1)

class TestppSenderChannel(unittest.TestCase):

    @patch.object(pingpong.socket, 'recv', new=mock_async_method(return_value=token))
    def test_receive_no_exception(self):
        actual = run(pingpong.receive(token))
        self.assertEqual((0,1), actual)
        pingpong.socket.close()

    @patch.object(pingpong.socket, 'recv', new=mock_async_method(return_value=None))
    @patch.object(pingpong.socket, 'send', side_effect=Exception('timeout'))
    def test_receive_with_exception(self, mock_send):
        with self.assertRaises(Exception):
            run(pingpong.receive(token))
        pingpong.socket.close()

if __name__ == '__main__':
    unittest.main()
