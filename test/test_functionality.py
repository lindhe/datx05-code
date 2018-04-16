import unittest
import struct
import os
from client import Client

class TestFunctionality(unittest.TestCase):
    
    def setUp(self):
        self.c = Client('config/local.ini')
        self.c.read()

    def test_read_write(self):
        for i in range(50): 
            expected = os.urandom(1024)
            self.c.write(expected)
            actual = self.c.read()
            self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
