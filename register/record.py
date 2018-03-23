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

  def __eq__(self, other):
    return self.tag == other.tag\
        and self.element == other.element\
        and self.phase == other.phase

  def __hash__(self):
    return hash( (self.tag, self.element, self.phase) )
