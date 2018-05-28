#!/bin/python3.6

import os
import sys
from cas.old.cas import cas as Client


def main():
    msg_size = 512*1024
    cfgfile = sys.argv[1]
    c = Client(cfgfile, verbose=True)
    msg = os.urandom(msg_size)
    c.write(msg)
    print(f"Wrote {msg_size} bytes to quorum system.")

if __name__ == '__main__':
    main()
