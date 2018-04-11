import sys
import math
import configparser

def main(filename, nbr_of_servers, f):
    k = nbr_of_servers - 2*f
    if(k < 1):
        raise Exception("Coded elements less than 1")
    config = configparser.ConfigParser()
    config['Nodes'] = {}
    base_port = 5550
    for i in range(nbr_of_servers):
        nodename = 'Node{}'.format(i)
        port = base_port + i
        config['Nodes'][nodename] = '127.0.0.1:{}'.format(port)

    config['General'] = {}
    config['General']['n'] = str(nbr_of_servers)
    config['General']['f'] = str(f)
    config['General']['e'] = '0'
    config['General']['storage_location'] = './.storage/'
    config['General']['storage_size'] = '10'
    config['General']['gossip_freq'] = '1'

    with open(filename, 'w') as cfgfile:
        config.write(cfgfile)

if __name__ == '__main__':
    filename = input('Filename: ') + '.ini'
    nbr_of_servers = int(input('Number of servers: '))
    f = int(input('Number of crash prone servers: '))
    main(filename, nbr_of_servers, f)
