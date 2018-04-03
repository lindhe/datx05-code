from channel.ppProtocol import PingPongMessage
import asyncio

class QuorumSend:
    def __init__(self):
        self.pongRx = {}
        self.Q = 2
        self.pingTx = None
        self.event = None
        self.aggregated = None

    async def phaseInit(self, m):
        self.pongRx.clear()
        self.pingTx = m
        self.event = asyncio.Event()
        await self.event.wait()
        x = self.aggregated
        self.aggregated = None
        return x

    async def departure(self, server_id, msg):
        print("pingpong arrival! ")
        if msg and (self.pingTx != None):
            if(msg.get_req_tag() == self.pingTx.get_tag() and
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

        return self.pingTx.get_bytes() if self.pingTx else None
