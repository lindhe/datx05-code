import struct
from channel.ppProtocol import PingPongMessage

class QuorumRecvAR:

    def __init__(self, server):
        self.server = server

    async def arrival(self, sender, payload):
        print("pingpong CALLBACK")
        msg_list = PingPongMessage.set_message(payload)
        msg_data = PingPongMessage(*msg_list)
        if msg_data:
            tag = msg_data.get_tag()
            data = msg_data.get_data()
            label = msg_data.get_label()
            mode = msg_data.get_mode()
            if (label == 'qry'):
                if (mode == 'read'):
                    res = await self.server.read_query()
                else:
                    res = self.server.write_query()
            elif (label == 'write'):
                res = await self.server.write(tag, data)
            elif (label == 'inform'):
                res = await self.server.inform(tag, data)
            else:
                return None
            new_msg = PingPongMessage(*res, mode, req_tag=msg_data.get_tag())
            return new_msg.get_bytes()
        else:
            print("Got empty message")
            return None
