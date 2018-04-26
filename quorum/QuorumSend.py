from channel.ppProtocol import PingPongMessage
import asyncio

class QuorumSend:
    def __init__(self, quorum_size):
        self.pongRx = {}
        self.Q = quorum_size
        self.replies = quorum_size
        self.pingTx = None
        self.event = None
        self.aggregated = None

    async def phaseInit(self, m, opt_size=None):
        if opt_size:
            self.replies = opt_size
        else:
            self.replies = self.Q
        self.pongRx.clear()
        if (type(m[1]) == list):
            self.pingTx = []
            for i in range(len(m[1])):
                self.pingTx.append(PingPongMessage(m[0], m[1][i], *m[2:]))
        else:
            self.pingTx = PingPongMessage(*m)
        self.event = asyncio.Event()
        await self.event.wait()
        x = self.aggregated
        self.aggregated = None
        return x

    async def departure(self, server_id, msg):
        if __debug__:
            print("pingpong arrival! ")
        if (type(self.pingTx) == list):
            pingTx = self.pingTx[server_id]
        else:
            pingTx = self.pingTx

        if msg and (pingTx != None):
            if(msg.get_req_tag() == pingTx.get_tag() and
               (msg.get_tag() == None or
               msg.get_label() == 'qry' or
               (msg.get_label() != 'qry' and
               (msg.get_tag() == msg.get_req_tag() and (
                msg.get_label() == pingTx.get_label())
              )))):
                self.pongRx[server_id] = msg
                if __debug__:
                    print("ADD to pongRx with size %s" % len(self.pongRx))
        elif not msg:
            self.pongRx.pop(server_id, None)

        if len(self.pongRx) >= self.replies:
            if __debug__:
                print("GOT ENOUGH elements")
            self.aggregated = list(self.pongRx.values())
            self.pongRx.clear()
            self.pingTx = None
            self.event.set()

        if (type(self.pingTx) == list):
            data = self.pingTx[server_id].get_bytes()
            return (data, not self.use_tcp(self.pingTx[server_id]))
        else:
            data = self.pingTx.get_bytes() if self.pingTx else None
            return (data, not self.use_tcp(self.pingTx))

    def use_tcp(self, tx):
        if not tx:
            return False
        if (len(tx.get_bytes()) > 1024):
           return True
        elif ((tx.get_label() == 'fin' or tx.get_label() == 'FIN') and tx.get_mode() == 'read'):
            return True
        else:
            return False
