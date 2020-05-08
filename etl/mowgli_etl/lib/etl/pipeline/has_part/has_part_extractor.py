from mowgli_etl.lib.etl._extractor import _Extractor
from mowgli_etl.lib.etl.pipeline_storage import PipelineStorage
from mowgli_etl.paths import DATA_DIR


class HasPartExtractor(_Extractor):
    __HAS_PART_KB_JSONL_BZ2_FILE_PATH = DATA_DIR / "has_part" / "extracted" / "hasPartKB.jsonl.bz2"

    def extract(self, *, force: bool, storage: PipelineStorage):
        return {
            "has_part_kb_jsonl_file_path": self._extract_bz2(force=force, path=self.__HAS_PART_KB_JSONL_BZ2_FILE_PATH,
                                                             storage=storage)}
