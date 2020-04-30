from abc import ABC


class _Closeable(ABC):
    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwds):
        self.close()
