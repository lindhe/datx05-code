import struct
from channel.ppProtocol import PingPongMessage

class QuorumRecv:

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
                    res = self.server.read_query()
                    if not res:
                        return None
                else:
                    res = self.server.write_query()
                    if not res:
                        return None
            elif (label == 'pre'):
                res = await self.server.pre_write(tag, data)
            elif (label == 'fin' or label == 'FIN'):
                if (mode == 'read'):
                    res = await self.server.read_finalize(tag, label)
                else:
                    res = await self.server.write_finalize(tag, label)
            elif (label == 'cntrQry'):
                res = self.server.counter_query(sender)
                if not res:
                    return None
            elif (label == 'incCntr'):
                nbr = struct.unpack("i", data)[0]
                res = self.server.set_counter(sender, nbr)
            else:
                return None
            new_msg = PingPongMessage(*res, mode, req_tag=msg_data.get_tag())
            return new_msg.get_bytes()
        else:
            print("Got empty message")
            return None
