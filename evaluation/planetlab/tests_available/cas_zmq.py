#!/bin/python3.5
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
from random import randint as rand
from time import sleep
from time import time
from cas.old.cas import cas as Client

def main(operation, rounds, config, step, msg_size):
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
  results['Times_write'] = {}
  results['Times_read'] = {}
  results['Average_write'] = {}
  results['Average_read'] = {}
  c = Client(config)
  # Add init record
  c.write(msg)
  print(f"Running {op} test at {uid}")
  for r in range(rounds):
    sleep(rand(0, max_delay)/1000)
    # DO WORK HERE
    time_in_write = time()
    c.write(msg)
    time_out_write = time() - time_in_write
    sleep(rand(0, max_delay)/1000)
    time_in_read = time()
    c.read()
    time_out_read = time() - time_in_read
    results['Times_write'][f"run{r}"] = str(time_out_write)
    results['Times_read'][f"run{r}"] = str(time_out_read)
  # Writer
  times_write = sorted([ float(v) for v in results['Times_write'].values() ])
  no_outliers_write = times_write[outliers:-outliers]
  results['Average_write']['average'] = str(sum(times_write) / (rounds))
  results['Average_write']['average_no_outliers'] = str(sum(no_outliers_write) / (rounds - 2*outliers))
  # Reader
  times_read = sorted([ float(v) for v in results['Times_read'].values() ])
  no_outliers_read = times_read[outliers:-outliers]
  results['Average_read']['average'] = str(sum(times_read) / (rounds))
  results['Average_read']['average_no_outliers'] = str(sum(no_outliers_read) / (rounds - 2*outliers))

  pathlib.Path(res).mkdir(exist_ok=True, parents=True)
  try:
    with open(res_file, 'a') as f:
      results.write(f)
    print(f"Write test done at {uid}!")
  except OSError as e:
    print(f"Error writing to file {res_file}: {e}", file=sys.stderr)

def to_bytes(s, prefix='b'):
  size = int(s)
  if (prefix == 'G'):
    return size*(2**30)
  elif (prefix == 'M'):
    return size*(2**20)
  elif (prefix == 'K'):
    return size*(2**10)
  else:
    return size

if __name__ == '__main__':
  program = sys.argv[0]
  if len(sys.argv) < 2:
    sys.exit()
  op = sys.argv[1]
  rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 20
  home=str(pathlib.Path.home())
  config = sys.argv[3] if len(sys.argv) > 3 else f"{home}/casss/config/autogen.ini"
  step_name = sys.argv[4] if len(sys.argv) > 4 else "step0"
  size = sys.argv[5] if len(sys.argv) > 5 else "512 K"
  msg_size = to_bytes(*size.split(' '))
  try:
    main(op, rounds, config, step_name, msg_size)
  except KeyboardInterrupt:
    sys.exit("\nInterrupted by ^C\n")
