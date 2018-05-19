#!/bin/python3.6
# -*- coding: utf-8 -*-
#
# License: MIT
# Author: Andreas Lindhé

import sys
import time
import os
from client import Client


def main(rounds=20):
  for r in range(rounds):
    print("It worked!")

#def main():
#    msg_size = 512*1024
#    cfgfile = sys.argv[1]
#    c = Client(cfgfile)
#    msg = os.urandom(msg_size)
#    c.write(msg)
#    print(f"Wrote {msg_size} bytes to quorum system.")

if __name__ == '__main__':
  program = sys.argv[0]
  rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 20
  try:
    main(rounds)
  except KeyboardInterrupt:
    sys.exit("\nInterrupted by ^C\n")
