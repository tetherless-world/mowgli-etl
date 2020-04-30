from mowgli.lib.storage._node_id_set import _NodeIdSet


class MemNodeIdSet(_NodeIdSet):
    def __init__(self):
        _NodeIdSet.__init__(self)
        self.__node_ids = set()

    def add(self, node_id: str) -> None:
        self.__node_ids.add(node_id)

    def __contains__(self, node_id: str):
        return node_id in self.__node_ids
