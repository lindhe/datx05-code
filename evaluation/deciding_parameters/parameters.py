#!/bin/python
# -*- coding: utf-8 -*-
#
# License: MIT
# Author: Andreas Lindhé

import sys
import math

def main(nmax=19, latex=False):
  n = nmax
  fmax = math.ceil(n/2)
  k_table(nmax, fmax, latex=latex)
  return

def k_table(nmax, fmax, latex=False):
  print(f"%%%%% Matrix for k value  %%%%%")
  matrix=[]
  matrix.append([' '])
  for i, n in enumerate(range(3, nmax+1)):
    matrix.append([n])
  for f in range(fmax +1):
    matrix[0].append(f)
    for i, n in enumerate(range(3, nmax+1)):
      kmax = n-2*f
      if kmax > 0:
        matrix[i+1].append(kmax)
  print_table(matrix, nmax, fmax, latex)
  return

def print_table(matrix, nmax, fmax, latex):
  if latex:
    for row in matrix:
      row_len = len(row)
      fmt = " {:>3} &"
      row_format = fmt * (row_len)
      for i in range(fmax - (row_len-1) +1):
        row.append('')
        row_format = row_format + fmt
      row_format = row_format + "\\\\"
      print(row_format.format( *row ))
  else:
    matrix.append(['n'])
    matrix[0].append('f')
    for row in matrix:
      row_format = "{:>2} " * len(row)
      print(row_format.format( *row ))

if __name__ == '__main__':
  program = sys.argv[0]
  latex=False
  if len(sys.argv) > 1:
    latex=True
  try:
    main(latex=latex)
  except KeyboardInterrupt:
    sys.exit("\nInterrupted by ^C\n")

