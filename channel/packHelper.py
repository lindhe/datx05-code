import struct

class PackHelper:

    '''
    Takes a number of variable length arguments and
    pack them into one byte object.
    '''
    def pack(self, *args, payload=None):
        h_pattern = ""
        for field in args:
            h_pattern += str(len(field))+"s"
        h_size = len(h_pattern.encode())
        tot_pattern = "i"+str(h_size)+"s"+h_pattern
        binary_data = struct.pack(tot_pattern, h_size,
                                  h_pattern.encode(), *args)
        if payload:
            binary_data += payload
        return binary_data

    '''
    Takes and parses a byte object and return
    the data on the form ((field1, field2,...) payload).
    '''
    def unpack(self, binary_data):
        int_size = struct.calcsize("i")
        pattern_size = struct.unpack("i", binary_data[:int_size])[0]
        pattern = str(pattern_size)+"s"
        h_pattern = struct.unpack(pattern,
                                  binary_data[int_size:int_size+pattern_size])[0]
        h_size = struct.calcsize(h_pattern)
        h_start = int_size+pattern_size
        h_fields = struct.unpack(h_pattern,
                                 binary_data[h_start:h_start+h_size])
        if(h_start+h_size < len(binary_data)):
            return (h_fields, binary_data[h_start+h_size:])
        else:
            return (h_fields,None)
