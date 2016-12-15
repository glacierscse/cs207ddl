import json

LENGTH_FIELD_LENGTH = 4


def serialize(json_obj):
    '''Turn a JSON object into bytes suitable for writing out to the network.
       Includes a fixed-width length field to simplify reconstruction on the other end of the wire.
       Param:
           json_obj: the JSON object.
       Return:
           bytes converted from the input JSON object.
    '''
    #your code here
    try:
        #j_obj = json.dumps(json_obj)
        #encode the information
        encode_obj = json_obj.encode()
        #length of the information
        string_len = len(encode_obj)
        encoded_string_len = int.to_bytes(string_len+LENGTH_FIELD_LENGTH,LENGTH_FIELD_LENGTH, byteorder = 'little')
        return encoded_string_len+encode_obj
    except:
        print('Invalid JSON object received:\n'+str(json_obj))
        return None


class Deserializer(object):
    '''A buffering and bytes-to-json engine.
       Data can be received in arbitrary chunks of bytes, and we need a way to
       reconstruct variable-length JSON objects from that interface. This class
       buffers up bytes until it can detect that it has a full JSON object (via
       a length field pulled off the wire). To use this, shove bytes in with the
       append() function and call ready() to check if we've reconstructed a JSON
       object. If True, then call deserialize to return it. That object will be
       removed from this buffer after it is returned.


       Implements:

           object.


       Attributes:

           buf: buffer.
           buflen: length of buffer.


       Methods:

           append: The function that shoves bytes in from the received chunks of bytes.
           ready: The function to check if we've reconstructed a JSON object.
           deserialize: The function to return a JSON object if we have reconstructed one.
    '''

    def __init__(self):
        '''The constructor to initialize a Deserializer object. 
        '''
        self.buf = b''
        self.buflen = -1

    def append(self, data):
        '''The function that shoves bytes in from the received chunks of bytes.
           Param:
               data: the data received in arbitrary chunks of bytes.
        ''' 
        self.buf += data
        self._maybe_set_length()

    def _maybe_set_length(self):
        '''The helper function of append function above.
        '''
        if self.buflen < 0 and len(self.buf) >= LENGTH_FIELD_LENGTH:
            self.buflen = int.from_bytes(self.buf[0:LENGTH_FIELD_LENGTH], byteorder="little")

    def ready(self):
        '''The function to check if we've reconstructed a JSON object.
           Return:
               true if we have reconstructed a JSON object;
               false otherwise.
        '''   
        return (self.buflen > 0 and len(self.buf) >= self.buflen)

    def deserialize(self):
        '''The function to return a JSON object if we have reconstructed one.
           The returned object will then be removed from buffer.
           Return:
               the reconstructed JSON object.
        '''
        json_str = self.buf[LENGTH_FIELD_LENGTH:self.buflen].decode()
        self.buf = self.buf[self.buflen:]
        self.buflen = -1
        # There may be more data in the buffer already, so preserve it
        self._maybe_set_length()
        try:
            #Note how now everything is assumed to be an OrderedDict
            obj = json.loads(json_str)
            print("OBJ", obj)
            return obj
        except json.JSONDecodeError:
            print('Invalid JSON object received:\n'+str(json_str))
            return None
