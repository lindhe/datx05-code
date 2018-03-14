import struct

class packHelper:

    '''
    Takes a number of variable length arguments and
    pack them into one byte object.
    '''
    def pack(self, *args, payload=None):
        hPattern = ""
        for field in args:
            hPattern += str(len(field))+"s"
        hSize = len(hPattern.encode())
        totPattern = "i"+str(hSize)+"s"+hPattern
        binaryData = struct.pack(totPattern, hSize,
                                 hPattern.encode(), *args)
        if payload:
            binaryData += payload
        return binaryData

    '''
    Takes and parses a byte object and return
    the data on the form ((field1, field2,...) payload).
    '''
    def unpack(self, binaryData):
        intSize = struct.calcsize("i")
        patternSize = struct.unpack("i", binaryData[:intSize])[0]
        pattern = str(patternSize)+"s"
        headerPattern = struct.unpack(pattern,
binaryData[intSize:intSize+patternSize])[0]
        headerSize = struct.calcsize(headerPattern)
        startHeader = intSize+patternSize
        headerFields = struct.unpack(headerPattern,
                                     binaryData[startHeader:startHeader+headerSize])
        if(startHeader+headerSize < len(binaryData)):
            return (headerFields, binaryData[startHeader+headerSize:])
        else:
            return (headerFields,None)
