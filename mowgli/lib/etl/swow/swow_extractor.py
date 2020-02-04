from mowgli.lib.etl._extractor import _Extractor

class SwowExtractor(_Extractor):
    def __init__(self, *, csv_file_path: str, **kwds):
        _Extractor.__init__(self)
        self.__csv_file_path = csv_file_path

    def extract(self, **kwds):
        self._logger.info("extract")
        return {"csv_file_path": self.__csv_file_path}
