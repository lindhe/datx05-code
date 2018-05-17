from channel.GossipProtocol import GossipMessage

class Gossip:

    def __init__(self, server):
        self.server = server

    async def departure(self, uid, msg_data):
        data = await self.server.gossip_departure(uid)
        return (data, not self.use_tcp(data))

    async def arrival(self, uid, payload):
        print("Gossip CALLBACK RECV")
        if payload:
            msg_list = GossipMessage.set_message(payload)
            msg_data = GossipMessage(*msg_list)
            print(msg_data.get_tag_tuple())
            await self.server.gossip_arrival(uid, *msg_data.get_tag_tuple(),
msg_data.get_prp(), msg_data.get_all(), msg_data.get_echo(), msg_data.get_cntrs())
        else:
            print("Got empty message")

    def use_tcp(self, tx):
        if not tx:
            return False
        if (len(tx) > 1024):
           return True
        else:
            return False
