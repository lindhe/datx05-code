from channel.ppProtocol import PingPongMessage

class ExamplePingPongSend:
    async def departure(self, msg_data):
        print("pingpong arrival!")
        if msg_data:
            print("Got message with label %s" % msg_data.get_label())
        else:
            print("Got empty message")
        pp_msg = PingPongMessage()
        msg = pp_msg.create_message(b'qry', b'bot',
                                    b'bot',b'none')
        return msg
