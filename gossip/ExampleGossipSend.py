from channel.GossipProtocol import GossipMessage

class ExampleGossipSend:
    async def callback(self, msg_data):
        print("Gossip CALLBACK SEND")
        tag_tuple = b'tag_tuple'
        prp = b'prp'
        msg_all = b'msg_all'
        echo = b'echo'
        uid = b'uid'
        gossip_obj = GossipMessage()
        return gossip_obj.create_message(tag_tuple, prp,
                                       msg_all, echo, uid)
