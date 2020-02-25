from mowgli.lib.etl._extractor import _Extractor

class WebchildExtractor(_Extractor):
    def __init__(self, *, memberof_csv_file_path: str, physical_csv_file_path: str, substanceof_csv_file_path: str, wordnet_csv_file_path: str, **kwds):
        _Extractor.__init__(self)
        self.__memberof_csv_file_path = memberof_csv_file_path
        self.__physical_csv_file_path = physical_csv_file_path
        self.__substanceof_csv_file_path = substanceof_csv_file_path
        self.__wordnet_csv_file_path = wordnet_csv_file_path

    def extract(self, **kwds):
        self._logger.info("extract")
        return {"csv_file_paths": [self.__memberof_csv_file_path, self.__physical_csv_file_path, self.__substanceof_csv_file_path, self.__wordnet_csv_file_path]}
