#!/bin/python
# -*- coding: utf-8 -*-
#
# License: MIT
# Author: Andreas Lindhé

class Register:

  """
  Update the set of stored records appropriately
  """
  def update_phase(self, tag, element, phase):
    return

  """
  Returns the correct phase:
  pre -> fin
  fin -> FIN
  FIN -> FIN
  """
  def upgrade_phase(old, new):
    return

  """
  returns the maximum t of all (t, *, p) recrods stored which has p=phase.
  """
  def max_phase(phase):
    return

  """
  return the tripple with max_phase of pre, fin and FIN records respectively
  """
  def tag_tuple():
    return
