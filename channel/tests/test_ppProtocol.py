import unittest
import struct
from channel.ppProtocol import PingPongMessage

class TestPingPongMessage(unittest.TestCase):

    def test_pingpong_message(self):
        tag = (1, (1, None))
        label = 'label'
        mode = 'read'
        payload = b'payload'
        pp_msg = PingPongMessage(tag, payload, label, mode)
        self.assertEqual(tag, pp_msg.get_tag())
        self.assertEqual(label, pp_msg.get_label())
        self.assertEqual(mode, pp_msg.get_mode())
        self.assertEqual(payload, pp_msg.get_data())

if __name__ == '__main__':
    unittest.main()
