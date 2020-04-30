from mowgli.lib.storage._leveldb import _Leveldb


class PersistentNodeIdSet(_Leveldb):
    def add(self, node_id: str) -> None:
        key = self.__key(node_id=node_id)
        value = b''
        self._db.put(key, value)

    def __contains__(self, node_id: str):
        key = self.__key(node_id=node_id)
        value = self._db.get(key)
        return value is not None

    def __key(self, *, node_id: str) -> bytes:
        return node_id.encode("utf-8")
