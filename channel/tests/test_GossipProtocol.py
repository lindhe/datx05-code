import unittest
import struct
from GossipProtocol import GossipMessage

class TestGossipMessage(unittest.TestCase):

    def test_gossip_message(self):
        tag_tuple = b'tag_tuple'
        prp = b'prp'
        msg_all = b'msg_all'
        echo = b'echo'
        uid = b'uid'
        gossip_obj = GossipMessage()
        gossip_msg = gossip_obj.create_message(tag_tuple, prp,
                                       msg_all, echo, uid)
        gossip_obj.set_message(gossip_msg)
        self.assertEqual(tag_tuple, gossip_obj.get_tag_tuple())
        self.assertEqual(prp, gossip_obj.get_prp())
        self.assertEqual(msg_all, gossip_obj.get_all())
        self.assertEqual(echo, gossip_obj.get_echo())
        self.assertEqual(uid, gossip_obj.get_id())

if __name__ == '__main__':
    unittest.main()
