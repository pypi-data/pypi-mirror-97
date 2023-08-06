from .constants import MESSAGE_NOT_FOUND, STATUS_NOT_FOUND


class ResponseWriter():
    def __init__(self, scope):
        self._body = MESSAGE_NOT_FOUND.encode()
        self._headers = []
        self._status = STATUS_NOT_FOUND
    
    @property
    def body(self):
        return self._body
    
    @body.setter
    def body(self, value):
        self._body = value
    
    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        self._headers.append(value)

    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, value: int):
        self._status = value
