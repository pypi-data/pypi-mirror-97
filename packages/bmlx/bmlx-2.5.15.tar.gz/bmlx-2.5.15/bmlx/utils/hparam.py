class HParam(object):
    """Wrapper class to help migrate from contrib.HParam to new data structure."""

    def __init__(self, **kwargs):
        self._data = kwargs

    def __getitem__(self, key):
        return self._data[key]

    def __getattr__(self, key):
        return self._data[key]
