import struct

class PackHelper:
    """ Class to convert from and to a byte object """

    def pack(self, *args, payload=None):
        """ Takes a number of variable length arguments and
        pack them into one byte object. """
        header_fields = [x if x is not None else b'' for x in args]
        h_pattern = ""
        for field in header_fields:
            h_pattern += str(len(field))+"s"
        h_size = len(h_pattern.encode())
        tot_pattern = "i"+str(h_size)+"s"+h_pattern
        binary_data = struct.pack(tot_pattern, h_size,
                                  h_pattern.encode(), *header_fields)
        if payload:
            binary_data += payload
        return binary_data

    def unpack(self, binary_data):
        """ Takes and parses a byte object and return
        the data on the form ((field1, field2,...) payload). """
        int_size = struct.calcsize("i")
        pattern_size = struct.unpack("i", binary_data[:int_size])[0]
        pattern = str(pattern_size)+"s"
        h_pattern = struct.unpack(pattern,
                                  binary_data[int_size:int_size+pattern_size])[0]
        h_size = struct.calcsize(h_pattern)
        h_start = int_size+pattern_size
        h_fields = struct.unpack(h_pattern,
                                 binary_data[h_start:h_start+h_size])
        header_fields = [x if x is not b'' else None for x in h_fields]
        if(h_start+h_size < len(binary_data)):
            return (header_fields, binary_data[h_start+h_size:])
        else:
            return (header_fields,None)
