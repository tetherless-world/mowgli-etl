from mowgli_etl.storage._node_id_set import _NodeIdSet


class MemNodeIdSet(_NodeIdSet):
    def __init__(self):
        _NodeIdSet.__init__(self)
        self.__node_ids = set()

    def add(self, node_id: str) -> None:
        self.__node_ids.add(node_id)

    def close(self):
        pass

    def __contains__(self, node_id: str):
        return node_id in self.__node_ids

    @classmethod
    def temporary(cls):
        return cls()
