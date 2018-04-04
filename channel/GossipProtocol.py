from .packHelper import PackHelper
from ast import literal_eval

class GossipMessage:

    pack_helper = PackHelper()
    
    def __init__(self, tag_tuple, prp=None, msg_all=None, echo=None):
        self.tag_tuple = str(tag_tuple).encode() if type(tag_tuple) != bytes else tag_tuple
        self.prp = str(prp).encode() if type(prp) != bytes else prp
        self.msg_all = str(msg_all).encode() if type(msg_all) != bytes else msg_all
        self.echo = str(echo).encode() if type(echo) != bytes else echo

    def set_message(msg):
        res_tuple = GossipMessage.pack_helper.unpack(msg)
        ctrl_data = res_tuple[0]
        tag_tuple = ctrl_data[0]
        prp = ctrl_data[1]
        msg_all = ctrl_data[2]
        echo = ctrl_data[3]
        return [tag_tuple, prp, msg_all, echo]

    def get_bytes(self):
        msg = GossipMessage. \
              pack_helper.pack(self.tag_tuple, self.prp, self.msg_all, self.echo)
        return msg

    def get_tag_tuple(self):
        return literal_eval(self.tag_tuple.decode())

    def get_prp(self):
        return literal_eval(self.prp.decode())

    def get_all(self):
        return literal_eval(self.msg_all.decode())

    def get_echo(self):
        return literal_eval(self.echo.decode())
