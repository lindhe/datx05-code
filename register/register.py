#!/bin/python
# -*- coding: utf-8 -*-
#
# License: MIT
# Author: Andreas Lindhé

from record import Record


class Register:
  """ Implementation of the register which stores recrods """

  def __init__(self):
    # TODO: These are just temporary: should be removed.
    test = Record(0, "null", 0)
    self.registers = {0: test}

  """
  Update the set of stored records appropriately
  """
  def update_phase(self, tag, element, phase):
    S = self.registers
    if (tag in S) and S[tag].element and element:
      w = S[tag].element
      current_phase = S[tag].phase
      p = self.upgrade_phase(current_phase, phase)
      S[tag] = Record(tag, w, p)
    else:
      S[tag] = Record(tag, element, phase)

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
  def max_phase(self, phases):
    S = self.registers
    phase_tags = []
    for tag in S:
      if S[tag].phase in phases:
        phase_tags.append(tag)
    return max(phase_tags)

  """
  return the tripple with max_phase of pre, fin and FIN records respectively
  """
  def tag_tuple(self):
    max_all = self.max_phase(['pre', 'fin', 'FIN'])
    max_finFIN = self.max_phase(['fin', 'FIN'])
    max_FIN = self.max_phase(['FIN'])
    return (max_all, max_finFIN, max_FIN)
