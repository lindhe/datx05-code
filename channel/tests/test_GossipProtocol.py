import unittest
import struct
from channel.GossipProtocol import GossipMessage

class TestGossipMessage(unittest.TestCase):

    def test_gossip_message(self):
        tag_tuple = ((3, (2, None)), (2, (2, None)), (1, (2, None)))
        prp = (1, None)
        msg_all = False
        echo = (prp, msg_all)
        gossip_msg = GossipMessage(tag_tuple, prp, msg_all, echo)
        self.assertEqual(tag_tuple, gossip_msg.get_tag_tuple())
        self.assertEqual(prp, gossip_msg.get_prp())
        self.assertEqual(msg_all, gossip_msg.get_all())
        self.assertEqual(echo, gossip_msg.get_echo())

if __name__ == '__main__':
    unittest.main()
