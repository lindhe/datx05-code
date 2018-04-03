#!/bin/python
# -*- coding: utf-8 -*-
#
# MIT License
#
# Copyright (c) 2018 Robert Gustafsson
# Copyright (c) 2018 Andreas Lindhé
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from .record import Record
from .fileHelper import *


class Register:
  """ Implementation of the register which stores recrods """

  def __init__(self, storage_location="./.storage/"):
    """ Initiates a register with no records.
    register is a dict of Record objects: {(tag, element, phase)}
    tag is a tuple of (seq, uid)
    element is either None or a file path
    phase is either 'pre', 'fin' or 'FIN'.

    Args:
      storage_location (string, optional): path to storage location for elements
    """
    self.register = {}
    self.t0 = (0, None)
    self.storage_location = storage_location

  def __repr__(self):
    """ String representation prints the entire register dict """
    return repr( self.register )

  def __contains__(self, r):
    return r in self.register

  def update_phase(self, tag, element, phase):
    """ Update the set of stored records appropriately.

    If element is not None, we store it in a file and stores just the filepath
    in the Record.

    Args:
      tag (tuple): Sequence number and UID
      element (Maybe None): If not none, it's the coded element to be stored.
      phase (string): 'pre', 'fin' or 'FIN'
    """
    S = self.register
    if (tag in S) and S[tag].element and not element:
      w = S[tag].element
      current_phase = S[tag].phase
      p = self.upgrade_phase(current_phase, phase)
      S[tag] = Record(tag, w, p)
    else:
      # If element is not None, we write it to a file and use the path instead
      if element:
        filename = self.tag_to_filename(tag)
        element = write_file(element, filename, path=self.storage_location)
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
    if not phase_tags:
        return self.t0
    return max(phase_tags)

  def tag_tuple(self):
    """ return the tripple with max_phase of pre, fin and FIN records respectively """
    max_all = self.max_phase(['pre', 'fin', 'FIN'])
    max_finFIN = self.max_phase(['fin', 'FIN'])
    max_FIN = self.max_phase(['FIN'])
    return (max_all, max_finFIN, max_FIN)

  def fetch(self, tag):
    """ Reads a coded element from disk (if it exists).

    If there exists a Record with tag=tag, and its element is non-empty,
    we will read the element from disk and return it. Otherwise, None is
    returned.

    Args:
      tag (tuple): Sequence number and UID.
    Returns:
      Coded element if it exists on disk,
      None otherwise.
    """
    S = self.register
    if tag in S:
      element = S[tag].element
      if element:
        filename = self.tag_to_filename(tag)
        element = read_file(filename, path=self.storage_location)
      return element
    else:
      return None

  def tag_to_filename(self, tag):
    return '-'.join( [str(t) for t in tag] ) + '.elem'
