class CgiResponse:
    def __init__(self, header, data):
        self._header = header
        self._data = data

    @property
    def header(self):
        return _header

    @property
    def data(self):
        return _data

    def print(self):
        # TODO: extend the whole header shpiel
        print(self.header)
        # TODO: format data... (?)
        print(self.data)


