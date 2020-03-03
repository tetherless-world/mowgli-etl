from mowgli.lib.etl._extractor import _Extractor
import zipfile
import pathlib
from os import path

class WebchildExtractor(_Extractor):
    def __init__(self, *, memberof_csv_file_path: str, physical_csv_file_path: str, substanceof_csv_file_path: str, wordnet_csv_file_path: str, **kwds):
        _Extractor.__init__(self)
        self.__memberof_csv_file_path = memberof_csv_file_path
        self.__physical_csv_file_path = physical_csv_file_path
        self.__substanceof_csv_file_path = substanceof_csv_file_path
        self.__wordnet_csv_file_path = wordnet_csv_file_path

    def extract(self, **kwds):
        self._logger.info("extract")

        destination = pathlib.Path(__file__).parent.absolute().parents[3].joinpath('data').joinpath('webchild')

        if (path.exists(str(self.__physical_csv_file_path)[:-3] + 'txt')):
            self._logger.info("zip already extracted")
        else:
            with zipfile.ZipFile(self.__physical_csv_file_path) as zf:
                self._logger.info("extracting zip")
                zf.extractall(destination)
                self._logger.info("zip extracted")
                
        self.__physical_csv_file_path = str(self.__physical_csv_file_path)[:-3] + 'txt'
        return {"memberof_csv_file_path": self.__memberof_csv_file_path, "physical_csv_file_path": self.__physical_csv_file_path, "substanceof_csv_file_path" : self.__substanceof_csv_file_path, "wordnet_csv_file_path": self.__wordnet_csv_file_path}

