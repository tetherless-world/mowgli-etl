from typing import Optional

from mowgli.lib.etl._extractor import _Extractor
from mowgli.lib.etl.pipeline_storage import PipelineStorage


class WebChildExtractor(_Extractor):
    __PART_WHOLE_URL = "http://people.mpi-inf.mpg.de/~ntandon/resources/relations/partOf/webchild_partof.zip"
    __WORDNET_SENSES_URL = (
        "http://people.mpi-inf.mpg.de/~ntandon/resources/relations/metadata/noun.gloss"
    )
    __MEMBER_OF_FILENAME = "webchild_partof_memberof.txt"
    __PHYSICAL_FILENAME = "webchild_partof_physical.txt"
    __SUBSTANCEOF_FILENAME = "webchild_partof_substanceof.txt"

    def __init__(
        self,
        *,
        part_whole_url: Optional[str] = __PART_WHOLE_URL,
        wordnet_sense_url: Optional[str] = __WORDNET_SENSES_URL,
        memberof_filename: Optional[str] = __MEMBER_OF_FILENAME,
        physical_filename: Optional[str] = __PHYSICAL_FILENAME,
        substanceof_filename: Optional[str] = __SUBSTANCEOF_FILENAME,
        **kwds
    ):
        self.__part_whole_url = part_whole_url
        self.__wordnet_sense_url = wordnet_sense_url
        self.__memberof_filename = memberof_filename
        self.__physical_filename = physical_filename
        self.__substanceof_filename = substanceof_filename
        _Extractor.__init__(self, **kwds)

    def extract(self, *, force: bool, storage: PipelineStorage, **kwargs):
        self._logger.info("Extracting WebChild data")

        part_whole_archive_path = self._download(self.__part_whole_url, force, storage)
        zip_extractions = self._extract_zip(
            archive_path=part_whole_archive_path,
            filenames=(
                self.__memberof_filename,
                self.__physical_filename,
                self.__substanceof_filename,
            ),
            force=force,
            storage=storage,
        )
        memberof_csv_file_path = zip_extractions[self.__memberof_filename]
        physical_csv_file_path = zip_extractions[self.__physical_filename]
        substanceof_csv_file_path = zip_extractions[self.__substanceof_filename]

        wordnet_csv_file_path = self._download(self.__wordnet_sense_url, force, storage)

        return {
            "memberof_csv_file_path": memberof_csv_file_path,
            "physical_csv_file_path": physical_csv_file_path,
            "substanceof_csv_file_path": substanceof_csv_file_path,
            "wordnet_csv_file_path": wordnet_csv_file_path,
        }
