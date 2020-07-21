from pathlib import Path
from tempfile import mkdtemp

from mowgli_etl.storage._id_set import _IdSet
from mowgli_etl.storage.level_db import LevelDb


class PersistentIdSet(_IdSet):
    def __init__(self, **level_db_kwds):
        _IdSet.__init__(self)
        self.__level_db = LevelDb(**level_db_kwds)

    def add(self, id: str) -> None:
        key = self.__construct_key(id=id)
        value = b''
        self.__level_db.put(key, value)

    def close(self):
        self.__level_db.close()

    @property
    def closed(self):
        return self.__level_db.closed

    @staticmethod
    def __construct_key(id: str) -> bytes:
        return id.encode("utf-8")

    def __contains__(self, id: str):
        key = self.__construct_key(id=id)
        value = self.__level_db.get(key)
        return value is not None

    @classmethod
    def temporary(cls):
        return cls(directory_path=Path(mkdtemp()), delete_on_close=True)
