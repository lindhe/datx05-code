import timeit
import time
import datetime
import signal
import math
import sys
import os
import configparser
from client import Client
import pathlib

def now():
  return f"{datetime.datetime.now():%Y-%m-%d_%H:%M:%S}"

path = "./result/"

pathlib.Path(path).mkdir(exist_ok=True, parents=True)
result_file = path + now() + "-average_time.csv"

def note_result(writer_avg, reader_avg, file_size):
  result = f"\
File Size (B); {file_size}\n\
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

def main(file_sizes, rounds, iterations, cfgfile):
    c = Client(cfgfile)
    c.read()
    for size in file_sizes:
        value = os.urandom(size)
        writer = timeit.Timer(lambda:c.write(value))
        writer_avg = calcAvg(writer.repeat(rounds,iterations))
        reader = timeit.Timer(lambda:c.read())
        reader_avg = calcAvg(reader.repeat(rounds,iterations))
        note_result(writer_avg, reader_avg, size)

def calc_parameters(tcfile):
    config = configparser.ConfigParser()
    config.read(tcfile)
    start = config['Filesize']['start'].split()
    stop = config['Filesize']['stop'].split()
    increase = config['Filesize']['increase']
    step = config['Filesize']['step'].split()
    rounds = int(config['Filesize']['rounds'])
    iterations = int(config['Filesize']['iterations'])
    start_size = convert_to_bytes(*start)
    end_size = convert_to_bytes(*stop)
    delta = convert_to_bytes(*step)
    file_sizes = []
    current_size = start_size
    i = 0
    while (current_size < end_size):
        file_sizes.append(current_size)
        if (increase == 'linear'):
            current_size = start_size + (delta*i)
        else:
            current_size = start_size + (delta**i)
        i += 1
    return (file_sizes, rounds, iterations)

def convert_to_bytes(s, prefix='b'):
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
    tcfile = sys.argv[1]
    cfgfile = sys.argv[2]
    params = calc_parameters(tcfile)
    main(*params, cfgfile)
