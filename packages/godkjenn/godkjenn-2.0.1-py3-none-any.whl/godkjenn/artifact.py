class Artifact:
    """A single received or accepted piece of data.

    An artifact includes the byte data itself as well as
    any extra configuration it uses.
    """
    def __init__(self, data):
        self._data = data

    @property
    def data(self):
        "Data for the object (bytes)."
        return self._data

    def __eq__(self, rhs):
        return self.data == rhs.data
