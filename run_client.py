import sys
from client import Client

def main():
    cfgfile = sys.argv[1]
    c = Client(cfgfile)
    while True:
        op = input('Operation (read/write): ').split(' ', 1)
        if (op[0] == 'read'):
            res = c.read()
            print("CLIENT: %s" % res)
        elif (op[0] == 'write'):
            if len(op) < 2:
                msg = 'empty'.encode()
            else:
                msg = op[1].encode()
            c.write(msg)
            print("CLIENT: finished write operation")

if __name__ == '__main__':
    main()
