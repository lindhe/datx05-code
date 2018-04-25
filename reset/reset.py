#!/bin/python3.6
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

from register.register import Register
from proposal import Proposal as prp

class GlobalReset:
  """ Handle global reset (wrap-around) procedure. """

  def __init__(self, uid, config, register):
    """ Initialize the global reset procedure.

    Args:
      config (list): list of all servers in configuration
    """
    self.uid = uid
    self.config = config # List of uid
    self.dflt_prp = prp(0, None)
    self.prp = {} # {uid: Proposal} or {uid: None}
    self.all = []
    self.echo = []
    self.all_seen_processors = []
    self.register = register
    self.degrees = 6
    while True:
      if self.transient_fault():
        self.prp_set(None)
      # Update all[i]:
      (prp[uid], self.all[uid]) = (max_prp(), and_every(echo_no_all))
      if (prp[uid] == None and self.all[uid]):
        prp[uid] = self.dflt_prp
      if self.no_default_no_bot():
        for k in self.config:
          if (self.echo(k) and self.my_all(k)):
            all_seen_processors.append(k)
        if self.all_seen():
          (prp[uid], all_seen_processors) = (self.increment(prp[uid]), [])
        if prp[uid].phase == 2:
          self.local_reset(prp[uid].tag)

  def propose(self, tag):
    """ Proposes to reset register to only hold the Record with tag tag.

    Args:
      tag (tuple): tag to use as new ground truth
    """
    if enable_reset():
      prp[self.uid] = prp(1, tag)
    return

  def enable_reset(self):
    """ Blocks proposal if ongoing proposal.

    Returns:
      bool: True if good to go, False otherwise
    """
    return True

  def prp_set(self, val):
    """ Sets prp[k] to val for each k in self.config. """
    for k in self.config:
      prp[k] = None
    return

  def mod_max(self):
    """ Return the maximum phase of all proposals, in a modulus manner.

    Returns:
      int: a phase represented by 0, 1 or 2
    """
    phs = set()
    for k in self.config:
      phs.add(self.prp[k].phase)
    if not phs in set(0, 2):
      return max(phs)
    return 0

  def degree(self, k):
    """ Returns the degree of proposal k.

    Args:
      k (uid): which proposal to look at.
    Returns:
      int: the degree of prp[k]
    """
    return 2*prp[k].phase + (1 if my_all(k) else 0)

  def corr_deg(self, k, l):
    """ Returns whether the degrees of prp[k] and prp[l] correlates.

    Args:
      k, l (uid): The proposals to look at.
    Returns:
      bool: True if they correlate, False otherwise.
    """
    a = self.degree(k)
    b = self.degree(l)
    correlating_degrees = set()
    for i in range(self.degrees):
      correlating_degrees |= set([ (i, i), (i, (i+1)%self.degrees) ])
    return tuple(sorted((a, b))) in correlating_degrees

  def max_prp(self):
    """ Returns the maximal proposal.

    The loop does double duty: it collects a list of proposed tags, but will
    also return if phases are not synchronized.

    Returns:
      tuple: proposal
    """
    prp_tags = []
    for k in self.config:
      tags.append(self.prp[k].tag)
      if ((self.degree(k) - self.degree(self.uid))%self.degrees not in set(0, 1)):
        return self.prp[self.uid]
    return prp(self.mod_max(), max(prp_tags))

  def my_all(self, k):
    """ The myAll macro.

    Returns:
      bool: processor k is in all_seen_processors or all[k]==True
    """
    return k in self.all_seen_processors or self.all[k]

  def echo_no_all(self, k):
    """ Checks the echoed proposal from processor k.

    Args:
      k (uid): check last echo message from processor k
    Return
      bool: True if my proposal is the echoed proposal from processor k
    """
    return True

  def echo(self, k):
    """ Checks if my proposal and my_all variable are echoed by processor k.

    Args:
      k (uid): the processor which echo to check
    Returns:
      bool: True if my proposal and my_all are what's echoed back by processor
        k, false otherwise
    """
    return True

  def increment(self, proposal):
    """ Returns the appropriate incremented new proposal based on its phase.

    Args:
      prp (tuple): the proposal to increment.
    Returns:
      tuple: Proposal which is (2, prp) if prp.phase == 1, or self.dflt_prp
      otherwise.
    """
    return self.dflt_prp

  def all_seen(self):
    """ Reports if everyone have seen my proposal.

    Returns:
      bool: True if all is True and all active processors are in all_seen_processors
    """
    return True

  def proposal_set(self):
    """ Returns the set of all active proposals.

    Return:
      list: list of all proposals
    """
    return []

  def and_every(self, macro):
    """ Logical AND of every return value for macro[k] such that k is in config.

    Args:
      macro (function): macro must refer to a function which can take argument k
        and return a bool.
    Returns:
      bool: True if all macro[k]==True, False otherwise.
    """
    for k in self.config:
      if not macro(k):
        return False
    return True

  def transient_fault(self):
    """ Checks for all possible transient faults.

    Returns:
      bool: True if there is a transient fault detected, False otherwise.
    """
    return False

  def no_default_no_bot(self):
    """ Checks that no proposal holds dfltPrp or None (bot).

    Returns:
      bool: True if no proposal is dfltPrp and no proposal is None. False
        otherwise.
    """
    return False

  def local_reset(self, tag):
    """ Reset the local environment to only hold the Record with tag tag.

    Args:
      tag (tuple): the record to keep.
    """
    self.register.reset(tag)
    return
