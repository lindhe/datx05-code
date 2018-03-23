#!/bin/python
# -*- coding: utf-8 -*-
#
# License: MIT
# Author: Andreas Lindhé

from record import Record


class Register:
  """ Implementation of the register which stores recrods """

  def __init__(self):
    """ Initiates a register with no records """
    self.register = {}

  def __repr__(self):
    """ String representation prints the entire register dict """
    return str(self.register)

  def update_phase(self, tag, element, phase):
    """ Update the set of stored records appropriately """
    S = self.register
    if (tag in S) and S[tag].element and element:
      w = S[tag].element
      current_phase = S[tag].phase
      p = self.upgrade_phase(current_phase, phase)
      S[tag] = Record(tag, w, p)
    else:
      S[tag] = Record(tag, element, phase)

  def upgrade_phase(self, old, new):
    """
    Returns the correct phase:
    pre -> fin
    fin -> FIN
    FIN -> FIN
    """
    if (old == 'pre' and new == 'fin'):
      return 'fin'
    elif (old == 'fin' and new == 'FIN'):
      return 'FIN'
    else:
      return old

  def max_phase(self, phases):
    """
    returns the maximum t of all (t, *, p) recrods stored which has p=phase.
    Argument phases is a list of all phases which should be examined
    """
    S = self.register
    phase_tags = []
    for tag in S:
      if S[tag].phase in phases:
        phase_tags.append(tag)
    return max(phase_tags)

  def tag_tuple(self):
    """ return the tripple with max_phase of pre, fin and FIN records respectively """
    max_all = self.max_phase(['pre', 'fin', 'FIN'])
    max_finFIN = self.max_phase(['fin', 'FIN'])
    max_FIN = self.max_phase(['FIN'])
    return (max_all, max_finFIN, max_FIN)
