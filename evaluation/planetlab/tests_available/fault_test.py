#!/bin/python3.6
# -*- coding: utf-8 -*-
#
# License: MIT
#
##########################     RESET TEST     ##########################

import sys
import os
import pathlib
import configparser
from time import sleep
from time import time
from client import Client

def main(rounds, config, step):
  msg_size = 1024
  msg = os.urandom(msg_size)
  c = Client(config)
  for r in range(rounds):
    c.write(msg)
    msg = os.urandom(msg_size)
    print("Wrote record {}/{}".format(r, rounds))
  c.qrmAccess((None, None, 'fault', 'write'))
  print("Randomize sequence numbers")
  c.write(msg)
  actual = c.read()
  assert msg == actual 
  print("Test complete, wrote and read the same thing!")

if __name__ == '__main__':
  program = sys.argv[0]
  rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 5
  home=str(pathlib.Path.home())
  config = sys.argv[2] if len(sys.argv) > 2 else f"{home}/casss/config/local.ini"
  step_name = sys.argv[3] if len(sys.argv) > 3 else "step0"
  try:
    main(rounds, config, step_name)
  except KeyboardInterrupt:
    sys.exit("\nInterrupted by ^C\n")
