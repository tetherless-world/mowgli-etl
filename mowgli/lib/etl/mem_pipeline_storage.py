from io import StringIO, IOBase, BytesIO

from mowgli.lib.etl._pipeline_storage import _PipelineStorage


class MemPipelineStorage(_PipelineStorage):
    def __init__(self):
        self.__data = {}

    def get(self, key):
        return BytesIO(self.__data[key])

    def head(self, key):
        return key in self.__data

    def put(self, key, value):
        if isinstance(value, IOBase):
            value = value.read()
        if isinstance(value, str):
            value = value.encode("utf-8")
        assert isinstance(value, bytes), type(value)
        self.__data[key] = value

