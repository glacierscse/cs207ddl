import enum

class TSDBError(Exception):
    '''The TSDBError class in Python.
    '''
    pass

class TSDBOperationError(Exception):
    '''The TSDBOperationError class in Python.
    '''
    pass

class TSDBConnectionError(Exception):
    '''The TSDBConnectionError class in Python.
    '''
    pass

class TSDBStatus(enum.IntEnum):
    '''The TSDBStatus class in Python.
       The class member variables defines some representation of status.
    '''
    OK = 0
    UNKNOWN_ERROR = 1
    INVALID_OPERATION = 2
    INVALID_KEY = 3
    INVALID_COMPONENT = 4
    PYPE_ERROR = 5

    @staticmethod
    def encoded_length():
        return 3

    def encode(self):
        return str.encode('{:3d}'.format(self.value))

    @classmethod
    def from_bytes(cls, data):
        return cls(int(data.decode()))
