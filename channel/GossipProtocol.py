from packHelper import PackHelper

class GossipMessage:

    pack_helper = PackHelper()
    
    def create_message(self, tag_tuple, prp, msg_all, echo, uid):
        msg = GossipMessage. \
              pack_helper.pack(tag_tuple, prp, msg_all, echo, uid)
        return msg

    def set_message(self, msg):
        res_tuple = GossipMessage.pack_helper.unpack(msg)
        ctrl_data = res_tuple[0]
        self.tag_tuple = ctrl_data[0]
        self.prp = ctrl_data[1]
        self.all = ctrl_data[2]
        self.echo = ctrl_data[3]
        self.uid = ctrl_data[4]

    def get_tag_tuple(self):
        return self.tag_tuple

    def get_prp(self):
        return self.prp

    def get_all(self):
        return self.all

    def get_echo(self):
        return self.echo

    def get_id(self):
        return self.uid
