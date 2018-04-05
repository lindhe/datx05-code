from channel.ppProtocol import PingPongMessage
import asyncio

class QuorumSend:
    def __init__(self, quorum_size):
        self.pongRx = {}
        self.Q = quorum_size
        self.pingTx = None
        self.event = None
        self.aggregated = None

    async def phaseInit(self, m):
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
               (msg.get_tag() == msg.get_req_tag()
              )))):
                self.pongRx[server_id] = msg
                print("ADD to pongRx with size %s" % len(self.pongRx))
        elif not msg:
            self.pongRx.pop(server_id, None)

        if len(self.pongRx) >= self.Q:
            print("GOT ENOUGH elements")
            self.aggregated = list(self.pongRx.values())
            self.pongRx.clear()
            self.pingTx = None
            self.event.set()

        if (type(self.pingTx) == list):
            return self.pingTx[server_id].get_bytes()
        else:
            return self.pingTx.get_bytes() if self.pingTx else None
