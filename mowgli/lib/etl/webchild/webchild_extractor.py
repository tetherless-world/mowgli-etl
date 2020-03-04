from mowgli.lib.etl._extractor import _Extractor
import zipfile
import pathlib
from os import path
from mowgli.lib.etl.pipeline_storage import PipelineStorage
from mowgli.paths import DATA_DIR, SRC_ROOT, PROJECT_ROOT

class WebchildExtractor(_Extractor):
    def __init__(self, *, memberof_csv_file_path: str, physical_csv_file_path: str, substanceof_csv_file_path: str, wordnet_csv_file_path: str, **kwds):
        _Extractor.__init__(self)
        self.__memberof_csv_file_path = memberof_csv_file_path
        self.__physical_csv_file_path = physical_csv_file_path
        self.__substanceof_csv_file_path = substanceof_csv_file_path
        self.__wordnet_csv_file_path = wordnet_csv_file_path

    def extract(self, **kwds):
        self._logger.info("extract")

        if('data' in str(self.__physical_csv_file_path)):
            destination = DATA_DIR.joinpath('webchild')
        elif('mowgli_test' in str(self.__physical_csv_file_path)):
            destination = PROJECT_ROOT.joinpath('tests', 'mowgli_test', 'lib', 'etl', 'webchild')


        if (path.exists(str(self.__physical_csv_file_path)[:-3] + 'txt')):
            self._logger.info("zip already extracted")
        else:
            with zipfile.ZipFile(self.__physical_csv_file_path) as zf:
                self._logger.info("extracting zip")
                zf.extractall(destination)
                self._logger.info("zip extracted")

        self.__physical_csv_file_path = str(self.__physical_csv_file_path)[:-3] + 'txt'

        #when extract_zip works
        #destination = DATA_DIR.joinpath('webchild')
        #self.__physical_csv_file_path = self._extract_zip(force = False, storage = storage,from_url = from_url,target = destination)

        return {"memberof_csv_file_path": self.__memberof_csv_file_path, "physical_csv_file_path": self.__physical_csv_file_path, "substanceof_csv_file_path" : self.__substanceof_csv_file_path, "wordnet_csv_file_path": self.__wordnet_csv_file_path}

