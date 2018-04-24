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

class GlobalReset:
  """ Handle global reset (wrap-around) procedure. """

  def __init__(self, config):
    """ Initialize the global reset procedure.

    Args:
      config (list): list of all servers in configuration
    """
    self.config = config
    self.dflt_prp = (0, None)

  def propose(self, tag):
    """ Proposes to reset register to only hold the Record with tag tag.

    Args:
      tag (tuple): tag to use as new ground truth
    """
    if enable_reset():
      prp[i] = (1, tag)
    return

  def enable_reset(self):
    """ Blocks proposal if ongoing proposal.

    Returns:
      bool: True if good to go, False otherwise
    """
    return True

  def prp_set(self, val):
    """ Sets prp[k] to val for each k in self.config. """
    return

  def mod_max(self):
    """ Return the maximum phase of all proposals, in a modulus manner.

    Returns:
      int: a phase represented by 0, 1 or 2
    """
    return 0

  def degree(self, k):
    """ Returns the degree of proposal k.

    Args:
      k (uid): which proposal to look at.
    Returns:
      int: the degree of prp[k]
    """
    return 0

  def corr_deg(self, k, l):
    """ Returns whether the degrees of prp[k] and prp[l] correlates.

    Args:
      k, l (uid): The proposals to look at.
    Returns:
      bool: True if they correlate, False otherwise.
    """
    return True

  def max_prp(self):
    """ Returns the maximal proposal.

    Returns:
      tuple: proposal
    """
    return (0, None)

  def my_all(self, k):
    """ The myAll macro.

    Returns:
      bool: processor k is in all_seen_set or all[k]==True
    """
    return True

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

  def increment(self, prp):
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
      bool: True if all is True and all active processors are in all_seen
    """
    return True

  def proposal_set(self):
    """ Returns the set of all active proposals.

    Return:
      list: list of all proposals
    """
    return []
