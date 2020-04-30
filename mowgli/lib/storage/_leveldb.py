from pathlib import Path
from typing import Union

import plyvel


class _Leveldb:
    def __init__(self, *, name: Union[str, Path], create_if_missing=False, **kwds):
        self._db = plyvel.DB(name=str(name), create_if_missing=create_if_missing, **kwds)

    @property
    def closed(self):
        return self._db.closed

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwds):
        self._db.close()
