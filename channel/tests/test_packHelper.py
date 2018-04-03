import unittest
import struct
from ..packHelper import PackHelper

class TestPackHelperMethods(unittest.TestCase):

    def test_pack(self):
        tag = b'tag'
        label = b'label'
        uid = b'uid'
        payload = b'payload'
        pack_helper = PackHelper()

        actual = pack_helper.pack(tag, label, uid)
        expected = struct.pack("i6s3s5s3s", 6, b'3s5s3s',
                               tag, label, uid)
        self.assertEqual(expected, actual)

        actual = pack_helper.pack(tag, label, uid,
                                  payload=payload)
        expected += payload
        self.assertEqual(expected, actual)
        
    def test_unpack(self):
        tag = b'tag'
        label = b'label'
        uid = b'uid'
        payload = b'payload'
        pack_helper = PackHelper()

        actual = pack_helper.unpack(pack_helper.pack(tag, label, uid))
        expected = ((tag, label, uid), None)
        self.assertEqual(expected, actual)

        actual = pack_helper.unpack(pack_helper.pack(tag, label, uid,
                                                     payload=payload))
        expected = ((tag, label, uid), payload)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
