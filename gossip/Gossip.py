from channel.GossipProtocol import GossipMessage

class Gossip:

    def __init__(self, server):
        self.server = server

    async def departure(self, uid, msg_data):
        print("Gossip CALLBACK SEND")
        tag_tuple = self.server.get_tag_tuple()
        prp = (1,None)
        msg_all = False
        echo = (prp, msg_all)
        gossip_obj = GossipMessage(tag_tuple, prp, msg_all, echo)
        data = gossip_obj.get_bytes()
        return (data, not self.use_tcp(data))

    async def arrival(self, uid, msg_data):
        print("Gossip CALLBACK RECV")
        if msg_data:
            print("Got message with tag_tuple:")
            print(msg_data.get_tag_tuple())
            await self.server.gossip(uid, *msg_data.get_tag_tuple())
        else:
            print("Got empty message")

    def use_tcp(self, tx):
        if not tx:
            return False
        if (len(tx) > 1024):
           return True
        else:
            return False
