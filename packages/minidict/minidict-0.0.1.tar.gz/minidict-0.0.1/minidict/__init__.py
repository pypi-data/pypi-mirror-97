class minidict:
    """
    A slim read-only dictionary.
    """

    def __init__(self, data: dict):
        self._data = dict(data)

    def __repr__(self):
        return repr(self._data)

    def __getitem__(self, item):
        return self._data[item]

    def __len__(self):
        return len(self._data)

    def keys(self):
        return self._data.keys()

    def items(self):
        return zip(self._data.keys(), map(self.__getitem__, self._data.keys()))

    def __contains__(self, item):
        return (item in self._data)
