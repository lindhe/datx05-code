from .packHelper import PackHelper

class PingPongMessage:

    pack_helper = PackHelper()
    
    def __init__(self, tag, label, data, req_tag=None):
        self.tag = tag
        self.label = label
        self. data = data
        self.req_tag = req_tag

    def set_message(msg):
        res_tuple = PingPongMessage.pack_helper.unpack(msg)
        ctrl_data = res_tuple[0]
        data = res_tuple[1]
        tag = ctrl_data[0]
        label = ctrl_data[1]
        req_tag = ctrl_data[2]
        return [tag, label, data, req_tag]

    def get_bytes(self):
        msg = PingPongMessage. \
              pack_helper.pack(self.tag, self.label, self.req_tag, payload=self.data)
        return msg

    def is_bot(self):
        if (self.tag == None and self.label == None):
            return True
        else:
            return False

    def get_tag(self):
        return self.tag

    def get_data(self):
        return self.data

    def get_label(self):
        return self.label

    def get_id(self):
        return self.uid

    def get_req_tag(self):
        return self.req_tag
