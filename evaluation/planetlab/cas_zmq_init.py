#!/bin/python3.5

import os
import sys
from cas.old.cas import cas as Client


def main():
    msg_size = 512*1024
    cfgfile = sys.argv[1]
    c = Client(cfgfile, verbose=True)
    msg = os.urandom(msg_size)
    c.write(msg)
    print("Wrote {} bytes to quorum system.".format(msg_size))

if __name__ == '__main__':
    main()
