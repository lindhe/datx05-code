import zmq
import time
import signal
import math
import pathlib
from .cas import cas
from .server import server
from random import randint

def start_reader(ports, uid, verbose=False):
  ports = ports.split()
  s = cas(ports, uid, verbose)
  pathlib.Path('data').mkdir(exist_ok=True)
  filename = "data/reader-{0}.txt".format(str(uid))
  time.sleep(1)
  while True:
    try:
      val = s.read()
      if(val):
        f = open(filename, 'wb+')
        f.write(val)
      # print("READER: Latest value %s" % val)
      time.sleep(3)
    except KeyboardInterrupt:
      print("Ctrl-C")
      context.term()

def start_writer(ports, uid, datafile=None, verbose=False):
  ports = ports.split()
  s = cas(ports, uid, verbose)
  time.sleep(1)
  while True:
    try:
      if datafile:
        val = open(datafile, 'rb').read()
      else:
        val = b"test%d" % randint(0,1000)
      # print("val=%s" % val)
      s.write(val)
      time.sleep(1)
    except KeyboardInterrupt:
      print("Ctrl-C")
      context.term()

def start_server(port, addr, verbose=False):
  s = server(port, addr, verbose)
  s.start()
