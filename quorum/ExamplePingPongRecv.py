from channel.ppProtocol import PingPongMessage

class ExamplePingPongRecv:
    async def arrival(self, msg_data):
        print("pingpong CALLBACK")
        if msg_data:
            print("Got message with label %s" % msg_data.get_label())
            new_msg = PingPongMessage((1,(2,3)), b'bot',
                                     'qry', req_tag=msg_data.get_tag())
            return new_msg.get_bytes()
        else:
            print("Got empty message")
            return None
