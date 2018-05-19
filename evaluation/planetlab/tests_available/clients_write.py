#!/bin/python3.6
# -*- coding: utf-8 -*-
#
# License: MIT
# Author: Andreas Lindhé

import sys
import os
import pathlib
from random import randint as rand
from time import sleep
from time import time
from client import Client

msg_size = 512*1024
msg = os.urandom(msg_size)
# Random delay in ms
max_delay = 2000
op = 'write'
uid = os.uname().nodename
home=pathlib.Path.home()
res = str(home) + "/results/"
res_file = res + op + '_' + uid + '.csv'
outliers = 1

def main(rounds, config):
  acc_time = 0
  times = []
  c = Client(config)
  for r in range(rounds):
    sleep(rand(0, max_delay)/1000)
    print(f"Running {op} test at {uid}")
    time_in = time()
    # DO WORK HERE
    c.write(msg)
    time_out = time() - time_in
    times.append(time_out)
  times = sorted(times)
  no_outliers = times[1:-1]
  avg_time = sum(no_outliers) / (rounds - 2*outliers)
  avg_all = sum(times) / (rounds)
  result = str(time()) + '\t' \
      + op + ' ' + str(msg_size) + '\t'\
      + str(avg_time) + '\t' \
      + str(avg_all) + '\t' \
      + str(times) + '\t' \
      '\n'
  pathlib.Path(res).mkdir(exist_ok=True, parents=True)
  with open(res_file, 'a') as f:
    f.write(result)
  print(f"Wrote {msg_size} bytes to quorum system. It took {avg_time} seconds.")

if __name__ == '__main__':
  global config
  program = sys.argv[0]
  rounds = int(sys.argv[1]) if len(sys.argv) > 1 else rounds
  config = sys.argv[2] if len(sys.argv) > 2 else "~/casss/config/autogen.ini"
  try:
    main(rounds, config)
  except KeyboardInterrupt:
    sys.exit("\nInterrupted by ^C\n")
