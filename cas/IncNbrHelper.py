from collections import deque

class IncNbrHelper:
    def merge(q, l):
        for hw_addr, incnbr in l:
            if (hw_addr, None) in q:
                index = q.index((hw_addr, None))
                prev = q[index][1].nbr
                q.remove((hw_addr, None))
            else:
                prev = 0
            q.append((hw_addr, IncNbr(max(prev, incnbr))))

    def max_reached(q, m):
        for _, nbr in q:
            if nbr.nbr > m:
                return True
        return False

    def get(q, hw_addr):
        if (hw_addr, None) in q:
            index = q.index((hw_addr, None))
            tmp = q[index]
            q.remove((hw_addr, None))
            q.append(tmp)
            return tmp[1].nbr
        else:
            return 0

    def set(q, hw_addr, newIncNbr):
        if (hw_addr, None) in q:
            q.remove((hw_addr, None))
        q.append((hw_addr, IncNbr(newIncNbr)))

    def to_list(q):
        return [(a, b.nbr) for a, b in q]

class IncNbr:
    def __init__(self, nbr):
        self.nbr = nbr
    def __eq__(self, other):
        if not other:
            return True
        elif isinstance(self, other.__class__):
            return True
        else:
            return False
