from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp

import plyvel

from mowgli_etl._closeable import _Closeable


class LevelDb(_Closeable):
    def __init__(self, *, directory_path: Path, create_if_missing=True, delete_on_close=False, **kwds):
        self._db = plyvel.DB(name=str(directory_path), create_if_missing=create_if_missing, **kwds)
        self.__delete_on_close = delete_on_close
        self.__directory_path = directory_path

    @property
    def db(self) -> plyvel.DB:
        return self._db

    def close(self):
        self._db.close()
        if self.__delete_on_close:
            rmtree(self.__directory_path)

    @property
    def closed(self):
        return self._db.closed

    @classmethod
    def temporary(cls):
        return cls(directory_path=Path(mkdtemp()), delete_on_close=True)
