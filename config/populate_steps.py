#!/bin/python
# -*- coding: utf-8 -*-
#
# License: MIT
# Author: Andreas Lindhé

import sys
import time
import itertools
import pathlib

def main(r, w, c_nodes="clients.txt"):
  r = [int(e) for e in r]
  w = [int(e) for e in w]
  if len(r) == 1:
    r = r[0]
    with open(c_nodes) as f:
      client_nodes = f.read().splitlines()
      for writer in w:
        clients = r + writer
        client_list = (client_nodes*clients)[:clients]
        rs = client_list[:r]
        ws = client_list[-writer:]
        path = "tests/test-writers/" + "step" + str(writer) + '/'
        pathlib.Path(path).mkdir(exist_ok=True, parents=True)
        with open(path + "writers.txt", 'w') as f:
          for line in ws:
            f.write(line + '\n')
        with open(path + "readers.txt", 'w') as f:
          for line in rs:
            f.write(line + '\n')
  else:
    w = w[0]
    with open(c_nodes) as f:
      client_nodes = f.read().splitlines()
      for reader in r:
        clients = w + reader
        client_list = (client_nodes*clients)[:clients]
        rs = client_list[-reader:]
        ws = client_list[:w]
        path = "tests/test-readers/" + "step" + str(reader) + '/'
        pathlib.Path(path).mkdir(exist_ok=True, parents=True)
        with open(path + "writers.txt", 'w') as f:
          for line in ws:
            f.write(line + '\n')
        with open(path + "readers.txt", 'w') as f:
          for line in rs:
            f.write(line + '\n')

if __name__ == '__main__':
  program = sys.argv[0]
  readers = sys.argv[1].split(',')
  writers = sys.argv[2].split(',')
  try:
    main(readers, writers)
  except KeyboardInterrupt:
    sys.exit("\nInterrupted by ^C\n")

