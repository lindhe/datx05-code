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

from channel.ppProtocol import PingPongMessage
from register.record import Record
from register.register import Register


class Server:
  """ The event handlers for the server in Algorithm 2 """

  def __init__(self):
    """ Initialize with an empty register S """
    self.S = Register()

  def query(self, pp_msg):
    """ Reply to query arrival event, from pj's client to pi's server.

    Args:
      pp_msg (PingPongMessage): The arriving message.
    Returns:
      tuple (t, None, 'qry') where
        t is max_phase of ['fin', 'FIN'] for a read query and
        t is max_phase of ['pre', 'fin', 'FIN'] for a write query.
    """
    if pp_msg.mode == "read":
      phases = ['fin', 'FIN']
    else:
      phases = ['pre', 'fin', 'FIN']
    return (self.S.max_phase(phases), None, 'qry')

  def pre_write(self, pp_msg):
    """ Reply to pre-write arrival event, from pj's writer to pi's server.

    Args:
      pp_msg (PingPongMessage): The arriving message.
    Returns:
      A Record with (tag, None, 'pre').
    """
    tag = pp_msg.get_tag()
    element = pp_msg.get_data()
    phase = 'pre'
    self.S.update_phase(tag, element, phase)
    return Record(tag, None, phase)

  def finalize(self, pp_msg):
    """ Reply to fin or FIN arrival event, from pj's client to pi's server.

    Assumes that the message has phase 'fin' or 'FIN'.

    Args:
      pp_msg (PingPongMessage): The arriving message.
    Returns:
      Record(tag, element, phase) where element is ...
    """
    tag = pp_msg.get_tag()
    element = None
    phase = pp_msg.get_label()
    self.S.update_phase(tag, element, phase)
    if (pp_msg.mode = 'read') and (tag in S):
      element = S.fetch(tag).element
    return Record(tag, element, phase)

  def gossip(self):
    """ Reply to gossip arrival event, from pj's server to pi's server. """
    return
