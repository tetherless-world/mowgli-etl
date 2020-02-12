from mowgli.lib.etl._extractor import _Extractor

class WebchildExtractor(_Extractor):
    def __init__(self, *, csv_file_paths: list, **kwds):
        _Extractor.__init__(self)
        self.__csv_file_paths = csv_file_paths

    def extract(self, **kwds):
        self._logger.info("extract")
        return {"csv_file_paths": self.__csv_file_paths}
