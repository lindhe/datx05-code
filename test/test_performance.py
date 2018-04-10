import timeit
import time
import datetime
import signal
import math
import sys
import os
from client import Client

rounds = 1
iterations = 2

def now():
  return f"{datetime.datetime.now():%Y-%m-%d_%H:%M:%S}"

result_file = "./result/"+now()+"-average_time.csv"

def note_result(writer_avg, reader_avg, file_size):
  result = f"\
File Size (KiB); {file_size}\n\
Average Time writer; {writer_avg}\n\
Average Time reader; {reader_avg}\n\n"
  print(result)
  try:
    with open(result_file, 'a+') as f:
      f.write(result)
  except OSError as e:
    print(f"Could not write: {e}", file=sys.stderr)
    sys.exit(1)

def calcAvg(l):
    return float(sum(l)/(len(l)*1.0))

def main():
    c = Client() 
    c.read()
    for i in range(3):
        value = os.urandom(i*1024 + 1024)
        writer = timeit.Timer(lambda:c.write(value))
        writer_avg = calcAvg(writer.repeat(rounds,iterations))
        reader = timeit.Timer(lambda:c.read())
        reader_avg = calcAvg(reader.repeat(rounds,iterations))
        note_result(writer_avg, reader_avg, i+1)

if __name__ == '__main__':
    main()
