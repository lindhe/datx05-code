from channel.ppProtocol import PingPongMessage

class ExamplePingPongRecv:
    async def arrival(self, msg_data):
        print("pingpong CALLBACK")
        if msg_data:
            print("Got message with label %s" % msg_data.get_label())
        else:
            print("Got empty message")
        pp_msg = PingPongMessage()
        msg = pp_msg.create_message(b'qry2', b'bot',
                                    b'bot',b'none') 
        return msg
