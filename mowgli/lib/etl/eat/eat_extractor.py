from mowgli.lib.etl._extractor import _Extractor


class EatExtractor(_Extractor):
    def __init__(self, *, xml_file_path: str, **kwds):
        _Extractor.__init__(self)
        self.__xml_file_path = xml_file_path

    def extract(self, *, force, storage):
        self._logger.info("extract")
        return {"xml_file_path": self.__xml_file_path}
