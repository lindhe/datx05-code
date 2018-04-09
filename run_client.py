from client import Client

def main():
    c = Client()
    while True:
        op = input('Operation (read/write): ').split(' ', 1)
        if (op[0] == 'read'):
            res = c.read()
            print("CLIENT: %s" % res)
        elif (op[0] == 'write'):
            c.write(op[1].encode())
            print("CLIENT: finished write operation")

if __name__ == '__main__':
    main()
