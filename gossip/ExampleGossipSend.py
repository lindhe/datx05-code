from channel.GossipProtocol import GossipMessage

class ExampleGossipSend:
    async def departure(self, uid, msg_data):
        print("Gossip CALLBACK SEND")
        tag_tuple = ((2,(1,2)),(1,(1,2)),(1,(1,2)))
        prp = (1,None)
        msg_all = False
        echo = (prp, msg_all)
        gossip_obj = GossipMessage(tag_tuple, prp, msg_all, echo)
        return gossip_obj.get_bytes()
