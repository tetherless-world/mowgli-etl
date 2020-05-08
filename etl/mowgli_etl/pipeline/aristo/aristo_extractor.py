from mowgli_etl.lib.etl._extractor import _Extractor
from mowgli_etl.pipeline_storage import PipelineStorage
from mowgli_etl.paths import DATA_DIR


class AristoExtractor(_Extractor):
    __COMBINED_KB_TSV_BZ2_FILE_PATH = DATA_DIR / "aristo" / "extracted" / "COMBINED-KB.tsv.bz2"

    def extract(self, *, force: bool, storage: PipelineStorage):
        return {
            "combined_kb_tsv_file_path": self._extract_bz2(force=force,
                                                           path=self.__COMBINED_KB_TSV_BZ2_FILE_PATH,
                                                           storage=storage)}
