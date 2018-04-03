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
        return gossip_obj.get_bytes()

    async def arrival(self, uid, msg_data):
        print("Gossip CALLBACK RECV")
        if msg_data:
            print("Got message with tag_tuple:")
            print(msg_data.get_tag_tuple())
            self.server.gossip(uid, *msg_data.get_tag_tuple())
        else:
            print("Got empty message")
