import sys
import os
from client import Client

def main():
    cfgfile = sys.argv[1]
    c = Client(cfgfile)
    payload = os.urandom(200*(1024**2))
    while True:
        op = input('Operation (read/write): ').split(' ', 1)
        if (op[0] == 'read'):
            res = c.read()
            print("CLIENT: %s" % res)
        elif (op[0] == 'write'):
            c.write(payload)
            print("CLIENT: finished write operation")

if __name__ == '__main__':
    main()
