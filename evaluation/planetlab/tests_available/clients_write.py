#!/bin/python3.6
# -*- coding: utf-8 -*-
#
# License: MIT
# Author: Andreas Lindhé
#
##########################     CLIENT WRITE TEST     ##########################

import sys
import os
import pathlib
import configparser
import re
from random import randint as rand
from time import sleep
from time import time
from client import Client

def main(operation, rounds, config, step):
  msg_size = 512*1024
  msg = os.urandom(msg_size)
  # Random delay in ms
  max_delay = 2000
  op = operation
  uid = os.uname().nodename
  pid = str(os.getpid())
  home=pathlib.Path.home()
  res = str(home) + "/results/"
  scenario = step.split('/')[-1]
  res_file = res + scenario + '_' + op + '_' + uid + '.' + pid + '.log'
  outliers = 1
  if rounds - 2*outliers < 1:
    print("Can't have more outliers than rounds!", file=sys.stderr)
    rounds = 2*outliers + 1
  results = configparser.ConfigParser()
  acc_time = 0
  # Results
  results['Meta'] = {}
  results['Meta']['start_time'] = str(time())
  results['Meta']['uid'] = str(uid)
  results['Meta']['test'] = str(op)
  results['Meta']['rounds'] = str(rounds)
  results['Meta']['outliers'] = str(2*outliers)
  results['Meta']['file_size'] = str(msg_size)
  results['Times'] = {}
  results['Average'] = {}
  c = Client(config)
  for r in range(rounds):
    sleep(rand(0, max_delay)/1000)
    print(f"Running {op} test at {uid}")
    time_in = time()
    # DO WORK HERE
    if op == 'writer':
      c.write(msg)
    else:
      c.read()
    time_out = time() - time_in
    results['Times'][f"run{r}"] = str(time_out)
  times = sorted([ float(v) for v in results['Times'].values() ])
  no_outliers = times[outliers:-outliers]
  results['Average']['average'] = str(sum(times) / (rounds))
  results['Average']['average_no_outliers'] = str(sum(no_outliers) / (rounds - 2*outliers))
  if op == 'writer':
    pathlib.Path(res).mkdir(exist_ok=True, parents=True)
    try:
      with open(res_file, 'a') as f:
        results.write(f)
      print(f"Write test done!")
    except OSError as e:
      print(f"Error writing to file {res_file}: {e}", file=sys.stderr)

if __name__ == '__main__':
  program = sys.argv[0]
  if len(sys.argv) < 2:
    sys.exit()
  op = sys.argv[1]
  rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 20
  home=str(pathlib.Path.home())
  config = sys.argv[3] if len(sys.argv) > 3 else f"{home}/casss/config/autogen.ini"
  step_name = sys.argv[4] if len(sys.argv) > 4 else "step0"
  try:
    main(op, rounds, config, step_name)
  except KeyboardInterrupt:
    sys.exit("\nInterrupted by ^C\n")
