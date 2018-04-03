import unittest
import struct
import mock
import zmq
import asyncio
import pytest
from unittest.mock import patch
from ..ppProtocol import PingPongMessage
from ..SenderChannel import SenderChannel
from .unittest_helper import run, mock_async_method

class CallbackObj:
    async def callback(self):
        return "test"

pingpong = SenderChannel(0, CallbackObj(), "127.0.0.1", "5555")
token = struct.pack("ii", 0, 1)

class TestSenderChannel(unittest.TestCase):

    @patch.object(pingpong.socket, 'recv', new=mock_async_method(return_value=token))
    def test_receive_no_exception(self):
        actual = run(pingpong.receive(token))
        self.assertEqual((0, 1, None), actual)
        pingpong.socket.close()

    @patch.object(pingpong.socket, 'recv', new=mock_async_method(return_value=None))
    @patch.object(pingpong.socket, 'send_multipart', side_effect=Exception('timeout'))
    def test_receive_with_exception(self, mock_send):
        with self.assertRaises(Exception):
            run(pingpong.receive(token))
        pingpong.socket.close()

if __name__ == '__main__':
    unittest.main()
