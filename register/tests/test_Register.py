#!/bin/python
# -*- coding: utf-8 -*-
#
# License: MIT
# Author: Andreas Lindhé

import unittest
from record import Record
from register import Register

class TestRegister(unittest.TestCase):
  def setUp(self):
    self.s = Register()
    self.phases = ['pre', 'fin', 'FIN']

  def test_update_phase(self):
    """ Test that records can be updated correctly.
    1. Records added should be available.
    2. Another update with identical data should not change anything
    3. Records should be able to update phases 'pre' -> 'fin' -> 'FIN' but never
    any other way.
    """
    s = self.s
    # 1. If we add a record, that record can be found again.
    t1 = (1, 'a')
    w1 = '/tmp/asdf.txt'
    x = (t1, w1, 'pre')
    r1 = Record(*x)
    s.update_phase(*x)
    self.assertEqual( s.register[t1], r1 )
    # 2. Update with the same values should not change the register.
    s.update_phase(*x)
    self.assertEqual( s.register[t1], r1 )
    # 3. Only allow legal phase updates.
    x = (t1, w1, 'fin')
    r2 = Record(*x)
    # 3.1 Update existing record to phase 'fin'
    s.update_phase(*x)
    self.assertNotEqual( s.register[t1], r1 )
    self.assertEqual( s.register[t1], r2 )
    # 3.2 Try to change from 'fin' to 'pre', with element != None
    x = (t1, w1, 'pre')
    s.update_phase(*x)
    self.assertNotEqual( s.register[t1], r1 )
    self.assertEqual( s.register[t1], r2 )
    # 3.3 Try to change from 'fin' to 'pre', with element = None
    x = (t1, None, 'pre')
    s.update_phase(*x)
    self.assertEqual( s.register[t1].phase, 'pre')
    # 3.4 Try to change from 'pre' to 'FIN', with element != None
    x = (t1, w1, 'pre')
    s.update_phase(*x)
    x = (t1, w1, 'FIN')
    s.update_phase(*x)
    self.assertNotEqual( s.register[t1].phase, 'FIN')
    # 3.5 Try to change from 'pre' to 'fin' and then to 'FIN', with element != None
    x = (t1, w1, 'fin')
    s.update_phase(*x)
    x = (t1, w1, 'FIN')
    s.update_phase(*x)
    self.assertEqual( s.register[t1].phase, 'FIN')

  @unittest.skip("Skipping max_phase()")
  def test_max_phase(self):
    """ Test that the correct tag is returned for each set of phases.
    """
    return

  @unittest.skip("Skipping tag_tuple()")
  def test_tag_tuple(self):
    """ Test that the correct Record is returned for each set of phases.
    """
    return

if __name__ == '__main__':
  unittest.main()
