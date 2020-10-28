from mowgli_etl._extractor import _Extractor
from mowgli_etl.pipeline_storage import PipelineStorage


class GenericsKbExtractor(_Extractor):
    def extract(self, *, force: bool, storage: PipelineStorage):
        return {
            "tsv_file_path": storage.extracted_data_dir_path / "GenericsKB-Best.tsv"
        }
