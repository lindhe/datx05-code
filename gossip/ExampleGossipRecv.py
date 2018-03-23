from channel.GossipProtocol import GossipMessage

class ExampleGossipRecv:
    async def callback(self, msg_data):
        print("Gossip CALLBACK RECV")
        if msg_data:
            print("Got message with label %s" % msg_data.get_tag_tuple())
        else:
            print("Got empty message")
