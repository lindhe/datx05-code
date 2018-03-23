#!/bin/python
# -*- coding: utf-8 -*-
#
# License: MIT
# Author: Andreas Lindhé

import unittest
import itertools
from record import Record
from register import Register

class TestRegister(unittest.TestCase):
  def setUp(self):
    self.s = Register()
    self.phases = ['pre', 'fin', 'FIN']
    pre_max = 20
    fin_max = 12
    FIN_max = 6
    self.pre_max = pre_max
    self.fin_max = fin_max
    self.FIN_max = FIN_max
    for i in range(2, FIN_max):
      x = ((i, 'dflt'), None, 'FIN')
      r = Record(*x)
      self.s.update_phase(*x)
    for i in range(FIN_max, fin_max):
      x = ((i, 'dflt'), None, 'fin')
      r = Record(*x)
      self.s.update_phase(*x)
    for i in range(fin_max, pre_max):
      x = ((i, 'dflt'), None, 'pre')
      r = Record(*x)
      self.s.update_phase(*x)

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

  def test_max_phase(self):
    """ Test that the correct tag is returned for each set of phases.
    """
    s = self.s
    all_sets = []
    for i in range(len(self.phases)+1):
      all_sets += itertools.combinations(self.phases, i)
    all_sets = [list(a) for a in all_sets][1:]
    for D in all_sets:
      if 'pre' in D:
        self.assertEqual( s.max_phase(D)[0], self.pre_max-1)
      elif 'fin' in D:
        self.assertEqual( s.max_phase(D)[0], self.fin_max-1)
      else:
        self.assertEqual( s.max_phase(D)[0], self.FIN_max-1)

  @unittest.skip("Skipping tag_tuple()")
  def test_tag_tuple(self):
    """ Test that the correct Record is returned for each set of phases.
    """
    return

if __name__ == '__main__':
  unittest.main()
