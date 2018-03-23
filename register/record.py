#!/bin/python
# -*- coding: utf-8 -*-
#
# License: MIT
# Author: Andreas Lindhé

class Record:
  """ A record object class """

  def __init__(self, tag, element, phase):
    self.tag = tag
    self.element = element
    self.phase = phase

  def __repr__(self):
    return repr( (self.tag, self.element, self.phase) )
