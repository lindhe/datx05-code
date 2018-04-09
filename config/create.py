import sys
import math
import configparser

filename = input('Filename: ') + '.ini'
nbr_of_servers = int(input('Number of servers: '))
config = configparser.ConfigParser()
config['Nodes'] = {}
base_port = 5550
for i in range(nbr_of_servers):
    nodename = 'Node{}'.format(i)
    port = base_port + i
    config['Nodes'][nodename] = '127.0.0.1:{}'.format(port)

config['General'] = {}
config['General']['nodes'] = str(nbr_of_servers)
config['General']['quorumsize'] = str(math.floor(nbr_of_servers/2)+1)
config['General']['storage_location'] = './.storage/'
config['General']['storage_size'] = '10'

with open(filename, 'w') as cfgfile:
    config.write(cfgfile)
