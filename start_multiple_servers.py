import sys
import configparser
from multiprocessing import Process
import server

cfgfile = sys.argv[1]

config = configparser.ConfigParser()
config.read(cfgfile)

verbose = True
for node in config['Nodes']:
  ip, port = config['Nodes'][node].split(':')
  Process(target=server.main, args=[ip, port, cfgfile, verbose]).start()
  verbose = False
