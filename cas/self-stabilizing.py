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

from channel.GossipProtocol import GossipMessage
from channel.ppProtocol import PingPongMessage
from register.record import Record
from register.register import Register


class Server:
  """ The event handlers for the server in Algorithm 2 """

  def __init__(self, ip, port, quorum):
    self.uid = ip + ':' + str(port)
    # Quorum size:
    self.quorum = quorum
    # Initialize with an empty register S
    self.S = Register()
    # Received gossip messages. Key is UID and value is GossipMessage
    self.pre = {}
    self.fin = {}
    self.FIN = {}

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

  def pre_write(self, t, w):
    """ Reply to pre-write arrival event, from pj's writer to pi's server.

    Args:
      t (tuple): tag (Sequence number, UID)
      w (Byte): coded element
    Returns:
      (t, None, 'pre')
    """
    self.S.update_phase(t, w, 'pre')
    return (t, None, 'pre')

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

  def gossip(self, k, g_msg):
    """ Reply to gossip arrival event, from pj's server to pi's server.

    Updates the class variables pre, fin and FIN to include the content of the
    most recently received tag_tuple from a gossip from k.

    Args:
      k (uid): the UID of the server from which we received a gossip message
      g_msg (GossipMessage): the gossip message recevied from k with the tag_tuple
    Returns:
      tag_tuple(): (max_all, max_finFIN, max_FIN)
    """
    received_tags = g_msg.get_tag_tuple()
    (self.pre[k], self.fin[k], self.FIN[k]) = received_tags
    received_finFIN = (self.fin[k], self.FIN[k])
    received_finFIN = (self.FIN[k])
    i = self.uid
    # pre
    pre[i] = max( *received_tags, self.S.max_phase(['pre', 'fin', 'FIN']) )
    self.S.update_phase(pre[i], None, 'pre')
    # fin
    fin[i] = max( *received_finFIN, self.S.max_phase(['fin', 'FIN']) )
    self.S.update_phase(fin[i], None, 'fin')
    #FIN
    implicitFinalized = []
    fin_tags = [t for t in self.fin if t == self.fin[k]]
    if len(fin_tags) >= self.quorum:
      implicitFinalized = [self.fin[k]]
    FIN[i] = max( *received_FIN, self.S.max_phase(['FIN']), *implicitFinalized )
    self.S.update_phase(FIN[i], None, 'FIN')
    return self.S.tag_tuple()
