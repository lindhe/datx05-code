import unittest
import struct
from ppProtocol import PingPongMessage

class TestPingPongMessage(unittest.TestCase):

    def test_pingpong_message(self):
        tag = b'tag'
        label = b'label'
        uid = b'uid'
        payload = b'payload'
        pp_obj = PingPongMessage()
        pp_msg = pp_obj.create_message(label, tag,
                                       uid, payload)
        pp_obj.set_message(pp_msg)
        self.assertEqual(tag, pp_obj.get_tag())
        self.assertEqual(label, pp_obj.get_label())
        self.assertEqual(uid, pp_obj.get_id())
        self.assertEqual(payload, pp_obj.get_data())

if __name__ == '__main__':
    unittest.main()
