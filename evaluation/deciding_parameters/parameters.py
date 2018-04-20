#!/bin/python
# -*- coding: utf-8 -*-
#
# License: MIT
# Author: Andreas Lindhé

import sys
import time
import math
import numpy as np

def main(nmax=19):
  n = nmax
  fmax = math.ceil(n/2)

  # print(f"##### n={n} #####")
  # for k in range(1, n+1):
  #   fs = legal_f(n, k)
  #   print( "n={:>2}, k={:>2}: f={}".format(n, k, fs) )
  # for f in range( fmax +1 ):
  #   ks = legal_k(n, f)
  #   print( "n={:>2}, f={:>2}: k={}".format(n, f, ks) )

  print(f"##### Matrix for k value  #####")
  matrix=[]
  matrix.append([' '])
  for f in range(fmax +1):
    matrix[0].append(f)
  # By letting the limit=0, we print the maximal k
  limit=0
  for i, n in enumerate(range(3, nmax+1)):
    matrix.append([n])
    ks = legal_k(n, limit)
    ks.reverse()
    for k in ks[:fmax+1]:
      matrix[i+1].append(k)
  matrix[0].append('f')
  matrix.append(['n'])
  for row in matrix:
    row_format = "{:>2} " * len(row)
    print(row_format.format( *row ))
  return 0

def legal_k(n, f):
  return [ k for k in range(1, n-2*f +1) ]

def legal_f(n, k):
  return [ f for f in range(0, n +1) if n-2*f >= k-1 ]

if __name__ == '__main__':
  program = sys.argv[0]
  try:
    main()
  except KeyboardInterrupt:
    sys.exit("\nInterrupted by ^C\n")

