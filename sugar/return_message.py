

class Message(object):
    """
    JSON RETRUN MESSAGE CLASS
    sample message type
    {
        "status": "success",
        "data": "[] or {}",
        "message": "message or null"
    }
    """
    STATUS_TYPE = ['success', 'error', 'fail']

    def __init__(self, status, data=None, message=None):
        if status not in self.STATUS_TYPE:
            raise TypeError("status code error")
        self.status = status
        self.data = data
        self.message = message

    def __str__(self):
        return self.__dict__

    def __repr__(self):
        return self.__str__()

    def parse(self):
        return self.__str__()


def error_as_dict(_forms):
    _errors = {}
    for f in _forms:
        if f.errors:
            _errors[f.label or f.field] = [e for e in f.errors]
    return _errors
