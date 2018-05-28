import struct
import sys
import configparser
import math
import random as r
from CAS.server import server


def read_cfgfile(my_ip, my_port, cfgfile):
    my_addr = ":".join([my_ip, my_port])

    config = configparser.ConfigParser()
    config.read(cfgfile)
    nodes = list(config['Nodes'].values())


    nbr_of_servers = int(config['General']['n'])
    f = int(config['General']['f'])
    e = int(config['General']['e'])
    base_location = config['General']['storage_location']
    max_clients = int(config['General']['max_clients'])
    delta = int(config['General']['concurrent_clients'])
    queue_size = int(config['General']['queue_size'])
    gossip_freq = int(config['General']['gossip_freq'])
    chunks_size = int(config['General']['chunks_size'])
    return [nbr_of_servers, f, e, base_location, max_clients,
            delta, queue_size, gossip_freq, chunks_size, nodes]

def start(my_port, my_ip, nbr_of_servers, f, e, base_location, max_clients,
         delta, queue_size, gossip_freq, chunks_size, nodes):

    #print(my_ip, my_port)
    my_addr = my_ip + ':' + my_port
    other_nodes = [node for node in nodes if my_addr != node]

    print(other_nodes)
    s = server(my_addr, other_nodes)
    s.start()
    

def main(my_ip, my_port, cfgfile):
    parameters = read_cfgfile(my_ip, my_port, cfgfile)
    start(my_ip, my_port, *parameters)

if __name__ == '__main__':
    my_ip = sys.argv[1]
    my_port = sys.argv[2]
    cfgfile = sys.argv[3]
    main(my_port, my_ip, cfgfile)
