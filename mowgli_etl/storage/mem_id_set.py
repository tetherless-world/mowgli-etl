from mowgli_etl.storage._id_set import _IdSet


class MemIdSet(_IdSet):
    def __init__(self):
        _IdSet.__init__(self)
        self.__ids = set()

    def add(self, id: str) -> None:
        self.__ids.add(id)

    def close(self):
        pass

    def __contains__(self, id: str):
        return id in self.__ids

    @classmethod
    def temporary(cls):
        return cls()
