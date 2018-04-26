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
from .proposal import Proposal as Prp
from itertools import combinations
import time


class GlobalReset:
  """ Handle global reset (wrap-around) procedure. """

  def __init__(self, uid, config, register):
    """ Initialize the global reset procedure.

    Args:
      config (list): list of all servers in configuration
    """
    self.uid = uid
    self.register = register
    # Algorithm variables:
    self.config = config # List of uid
    self.prp = {} # {uid: Proposal} or {uid: None}
    self.all = {} # {uid: bool}
    self.echo_answers = {} # {uid: (prp, msg_all)}
    self.all_seen_processors = set()
    # Algorithm constants:
    self.dflt_prp = Prp(0, None)
    self.degrees = 6

  def main(self):
    # Main loop
    uid = self.uid
    while True:
      if self.transient_fault():
        self.prp_set(None)
      # Update all[i]:
      self.all[uid] = self.and_every(self.echo_no_all)
      if (self.prp[uid] == None and self.all[uid]):
        self.prp[uid] = self.dflt_prp
      if self.no_default_no_bot():
        self.prp[uid] = self.max_prp()
        for k in self.config:
          if (self.echo(k) and self.my_all(k)):
            self.all_seen_processors.add(k)
        if self.all_seen():
          (self.prp[uid], self.all_seen_processors) = \
              (self.increment(self.prp[uid]), set())
        if self.prp[uid].phase == 2:
          self.local_reset(self.prp[uid].tag)
      time.sleep(1)

  def propose(self, tag):
    """ Proposes to reset register to only hold the Record with tag tag.

    Args:
      tag (tuple): tag to use as new ground truth
    """
    if enable_reset():
      prp[self.uid] = Prp(1, tag)
    return

  def enable_reset(self):
    """ Blocks proposal if ongoing proposal.

    Returns:
      bool: True if good to go, False otherwise
    """
    for k in self.config:
      if self.prp[k] == None \
          or ((self.prp[k], self.all[k]) != (self.dflt_prp, True)):
        return False
    return True

  def prp_set(self, val):
    """ Sets prp[k] to val for each k in self.config. """
    for k in self.config:
      self.prp[k] = None
    return

  def mod_max(self):
    """ Return the maximum phase of all proposals, in a modulus manner.

    Returns:
      int: a phase represented by 0, 1 or 2
    """
    phs = set()
    for k in self.config:
      phs.add(self.prp[k].phase)
    if not phs in set([0, 2]):
      return max(phs)
    return 0

  def degree(self, k):
    """ Returns the degree of proposal k.

    Args:
      k (uid): which proposal to look at.
    Returns:
      int: the degree of prp[k]
    """
    return 2*self.prp[k].phase + (1 if self.my_all(k) else 0)

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
      if self.prp[k]:
        prp_tags.append(self.prp[k].tag)
        if ((self.degree(k) - self.degree(self.uid))%self.degrees not in set([0, 1])):
          return self.prp[self.uid]
      else:
        # If there was a None proposal, let's not progress
        return self.prp[self.uid]
    return Prp(self.mod_max(), max(prp_tags))

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
    return self.prp[self.uid] == self.echo_answers[k][0]

  def echo(self, k):
    """ Checks if my proposal and my_all variable are echoed by processor k.

    Args:
      k (uid): the processor which echo to check
    Returns:
      bool: True if my proposal and my_all are what's echoed back by processor
        k, false otherwise
    """
    return (self.prp[self.uid], self.my_all(self.uid)) == self.echo_answers[k]

  def increment(self, proposal):
    """ Returns the appropriate incremented new proposal based on its phase.

    Args:
      prp (tuple): the proposal to increment.
    Returns:
      tuple: Proposal which is (2, prp) if prp.phase == 1, or self.dflt_prp
      otherwise.
    """
    if proposal.phase == 1:
      return Prp(2, proposal.tag)
    return self.dflt_prp

  def all_seen(self):
    """ Reports if everyone have seen my proposal.

    Returns:
      bool: True if all is True and all active processors are in all_seen_processors
    """
    return self.all[self.uid] \
        and set(self.config) <= self.all_seen_processors | set(self.uid)

  def proposal_set(self):
    """ Returns the set of all active proposals.

    Set of proposed tags, if there is an l in config for which prp[l]=(2, *)

    Return:
      list: list of all proposals, or empty list
    """
    proposal_phases = [self.prp[k].phase if self.prp[k] else None for k in self.config]
    if 2 in proposal_phases:
      return set([self.prp[k].tag if self.prp[k] else None for k in self.config])
    else:
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
    # (∃pk ∈ config : prp[k] = ⊥)
    is_bot_prp = [k for k in self.config if self.prp[k] == None]
    # (prp[i] != {dfltPrp})
    prp_other_than_dflt = self.prp[self.uid] != self.dflt_prp
    if (is_bot_prp and prp_other_than_dflt):
      return True
    # (∃pk : ((prp[k] =< 0, s >) ∧ (s != ⊥))
    zero_s_not_bot = [self.prp[k] for k in self.config \
        if self.prp[k] and self.prp[k].tag and self.prp[k].phase == 0]
    # (∃pk, pk' ∈ config : ¬corrDeg(k, k'))
    differing_deg = False
    for k in combinations(self.config, 2):
      if not self.corr_deg(*k):
        differing_deg = True
    # {pk ∈ config : degree(i)+1 mod 6 = degree(k)}
    k_with_diff_deg = [k for k in self.config\
        if (self.degree(self.uid)+1 % self.degrees == self.degree(k))]
    # (k_with_diff_deg ⊆ allSeenProcessors)
    close_deg_seen = set(k_with_diff_deg) <= self.all_seen_processors \
        if k_with_diff_deg else False
    return zero_s_not_bot \
        or differing_deg \
        or close_deg_seen \
        or (len(self.proposal_set()) > 1)

  def no_default_no_bot(self):
    """ Checks that no proposal holds dfltPrp or None (bot).

    Returns:
      bool: True if no proposal is dfltPrp and no proposal is None. False
        otherwise.
    """
    phs = set([self.prp[k] for k in self.config])
    return (not phs.issubset(set([self.dflt_prp]))) and (None not in phs)

  def local_reset(self, tag):
    """ Reset the local environment to only hold the Record with tag tag.

    Args:
      tag (tuple): the record to keep.
    """
    self.register.reset(tag)
    return
