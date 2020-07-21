import pickle
from pathlib import Path
from tempfile import mkdtemp
from typing import Optional, Generator

from mowgli_etl.model.kg_node import KgNode
from mowgli_etl.storage._node_set import _NodeSet
from mowgli_etl.storage.level_db import LevelDb


class PersistentNodeSet(_NodeSet):
    def __init__(self, **level_db_kwds):
        _NodeSet.__init__(self)
        self.__level_db = LevelDb(**level_db_kwds)

    def add(self, node: KgNode) -> None:
        key = self.__construct_node_key(node.id)
        value = pickle.dumps(node)
        self.__level_db.put(key, value)

    def delete(self, node_id: str) -> None:
        key = self.__construct_node_key(node_id)
        self.__level_db.delete(key)

    def close(self):
        self.__level_db.close()

    @property
    def closed(self):
        return self.__level_db.closed

    @staticmethod
    def __construct_node_key(node_id: str) -> bytes:
        return node_id.encode("utf-8")

    def __contains__(self, node_id: str):
        key = self.__construct_node_key(node_id)
        value = self.__level_db.get(key)
        return value is not None

    def get(self, node_id: str, default: Optional[KgNode] = None) -> Optional[KgNode]:
        key = self.__construct_node_key(node_id)
        value = self.__level_db.get(key)
        if value is not None:
            return pickle.loads(value)
        else:
            return default

    def keys(self) -> Generator[str, None, None]:
        with self.__level_db.iterator(include_value=False) as it:
            for key in it:
                yield key.decode("utf-8")

    @classmethod
    def temporary(cls):
        return cls(directory_path=Path(mkdtemp()), delete_on_close=True)
