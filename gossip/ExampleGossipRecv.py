from channel.GossipProtocol import GossipMessage

class ExampleGossipRecv:
    async def arrival(self, msg_data):
        print("Gossip CALLBACK RECV")
        if msg_data:
            print("Got message with tag_tuple:")
            print(msg_data.get_tag_tuple())
        else:
            print("Got empty message")
