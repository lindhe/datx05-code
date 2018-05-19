#!/bin/python3.6
# -*- coding: utf-8 -*-
#
# License: MIT
# Author: Andreas Lindhé
#
###########################     CLIENT READ TEST     ###########################

import sys
import os
import pathlib
import configparser
from random import randint as rand
from time import sleep
from time import time
from client import Client

# Random delay in ms
max_delay = 2000
op = 'read'
uid = os.uname().nodename
home=pathlib.Path.home()
res = str(home) + "/results/"
res_file = res + op + '_' + uid + '.csv'
outliers = 1

def main(rounds, config):
  results = configparser.ConfigParser()
  acc_time = 0
  results['Meta'] = {}
  results['Meta']['start_time'] = str(time())
  results['Meta']['uid'] = str(uid)
  results['Meta']['test'] = str(op)
  results['Meta']['rounds'] = str(rounds)
  results['Meta']['outliers'] = str(rounds)
  results['Times'] = {}
  results['Average'] = {}
  c = Client(config)
  for r in range(rounds):
    sleep(rand(0, max_delay)/1000)
    print(f"Running {op} test at {uid}")
    time_in = time()
    # DO WORK HERE
    c.read()
    time_out = time() - time_in
    results['Times'][f"run{r}"] = str(time_out)
  times = sorted([ float(v) for v in results['Times'].values() ])
  no_outliers = times[1:-1]
  results['Average']['average'] = str(sum(times) / (rounds))
  results['Average']['average_no_outliers'] = str(sum(no_outliers) / (rounds - 2*outliers))
  pathlib.Path(res).mkdir(exist_ok=True, parents=True)
  with open(res_file, 'a') as f:
    results.write(f)
  print(f"Read test done!")

if __name__ == '__main__':
  global config
  program = sys.argv[0]
  rounds = int(sys.argv[1]) if len(sys.argv) > 1 else rounds
  config = sys.argv[2] if len(sys.argv) > 2 else "~/casss/config/autogen.ini"
  try:
    main(rounds, config)
  except KeyboardInterrupt:
    sys.exit("\nInterrupted by ^C\n")
