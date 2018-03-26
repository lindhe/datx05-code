from .packHelper import PackHelper

class PingPongMessage:

    pack_helper = PackHelper()
    
    def create_message(self, tag, label, uid, mode, data):
        msg = PingPongMessage. \
              pack_helper.pack(tag, label, uid, mode, payload=data)
        return msg

    def set_message(self, msg):
        res_tuple = PingPongMessage.pack_helper.unpack(msg)
        ctrl_data = res_tuple[0]
        self.data = res_tuple[1]
        self.label = ctrl_data[0]
        self.tag = ctrl_data[1]
        self.uid = ctrl_data[2]
        self.mode = ctrl_data[3]

    def get_tag(self):
        return self.tag

    def get_data(self):
        return self.data

    def get_label(self):
        return self.label

    def get_id(self):
        return self.uid

    def get_mode(self):
        """ Mode is 'write' or 'read' """
        return self.mode
