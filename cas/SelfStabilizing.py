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

  def __init__(self, uid, quorum, storage_location="./.storage/"):
    self.uid = uid
    # Quorum size:
    self.quorum = quorum
    # Initialize with an empty register S
    self.S = Register(storage_location)
    # Received gossip messages. Key is UID and value is tag
    self.pre = {}
    self.fin = {}
    self.FIN = {}

  def read_query(self):
    """ Reply to read query arrival event, from pj's client to pi's server.

    Returns:
      tuple (t, None, 'qry') where t is max_phase of ['fin', 'FIN']
    """
    return (self.S.max_phase(['fin', 'FIN']), None, 'qry')

  def write_query(self):
    """ Reply to write query arrival event, from pj's client to pi's server.

    Returns:
      tuple (t, None, 'qry') where t is max_phase of ['pre', 'fin', 'FIN']
    """
    return (self.S.max_phase(['pre', 'fin', 'FIN']), None, 'qry')

  async def pre_write(self, t, w):
    """ Reply to pre-write arrival event, from pj's writer to pi's server.

    Args:
      t (tuple): tag (Sequence number, UID)
      w (Byte): coded element
    Returns:
      (t, None, 'pre')
    """
    await self.S.update_phase(t, w, 'pre')
    return (t, None, 'pre')

  async def read_finalize(self, t, d):
    """ Update register and return a reply, for fin or FIN pp-arrival event.

    Args:
      t (tuple): tag (Sequence number, UID)
      d (string): phase 'fin' or 'FIN'
    Returns:
      tuple: (t, w, d) where w is the coded element if it exists in the record,
      or None otherwise.
    """
    await self.S.update_phase(t, None, d)
    w = await self.S.fetch(t)
    return (t, w, d)

  async def write_finalize(self, t, d):
    """ Update register and return a reply, for fin or FIN pp-arrival event.

    Args:
      t (tuple): tag (Sequence number, UID)
      d (string): phase 'fin' or 'FIN'
    Returns:
      tuple: (t, None, d)
    """
    await self.S.update_phase(t, None, d)
    return (t, None, d)

  async def gossip(self, k, pre, fin, FIN):
    """ Reply to gossip arrival event, from pj's server to pi's server.

    Updates the class variables pre, fin and FIN to include the content of the
    pre, fin and FIN received via a gossip message from server with uid k.

    Args:
      k (string): the UID of the server from which we received a gossip message
      pre (tuple): the pre[k] tag received in gossip[k]
      fin (tuple): the fin[k] tag received in gossip[k]
      FIN (tuple): the FIN[k] tag received in gossip[k]
    Returns:
      tag_tuple(): (max_all, max_finFIN, max_FIN)
    """
    # We need to store the received tag values, for the implicit FIN to work
    (self.pre[k], self.fin[k], self.FIN[k]) = (pre, fin, FIN)
    i = self.uid
    # pre
    self.pre[i] = max( pre, fin, FIN, self.S.max_phase(['pre', 'fin', 'FIN']) )
    await self.S.update_phase(self.pre[i], None, 'pre')
    # fin
    self.fin[i] = max( fin, FIN, self.S.max_phase(['fin', 'FIN']) )
    await self.S.update_phase(self.fin[i], None, 'fin')
    #FIN
    implicitFinalized = []
    fin_tags = [t for t in self.fin.values() if t == fin]
    if len(fin_tags) >= self.quorum:
      implicitFinalized = [fin]
    self.FIN[i] = max( FIN, self.S.max_phase(['FIN']), *implicitFinalized )
    await self.S.update_phase(self.FIN[i], None, 'FIN')

  def get_tag_tuple(self):
    return self.S.tag_tuple()
