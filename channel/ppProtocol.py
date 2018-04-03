from .packHelper import PackHelper
from ast import literal_eval

class PingPongMessage:

    pack_helper = PackHelper()
    
    def __init__(self, tag, label, data, req_tag=None):
        self.tag = str(tag).encode() if type(tag) != bytes else tag
        self.label = label.encode() if type(label) != bytes else label
        self.data = data
        self.req_tag = str(req_tag).encode() if type(req_tag) != bytes else req_tag

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

    def get_tag(self):
        return literal_eval(self.tag.decode())

    def get_data(self):
        return self.data

    def get_label(self):
        return self.label.decode()

    def get_req_tag(self):
        return literal_eval(self.req_tag.decode())

    def get_mode(self):
        """ Mode is 'write' or 'read' """
        return self.mode
