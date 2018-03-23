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
  def upgrade_phase(self, old, new):
    try:
      if (old == 'pre' and new == 'fin'):
        return 'fin'
      elif (old == 'fin' and new == 'FIN'):
        return 'FIN'
      else:
        return old
    except Exception as e:
      print(type(e))
      print("Error in upgrade_phase.")
      print(e)

  """
  returns the maximum t of all (t, *, p) recrods stored which has p=phase.
  Argument phases is a list of all phases which should be examined
  """
  def max_phase(phases):
    return

  """
  return the tripple with max_phase of pre, fin and FIN records respectively
  """
  def tag_tuple(self):
    max_all = self.max_phase(['pre', 'fin', 'FIN'])
    max_finFIN = self.max_phase(['fin', 'FIN'])
    max_FIN = self.max_phase(['FIN'])
    return (max_all, max_finFIN, max_FIN)
