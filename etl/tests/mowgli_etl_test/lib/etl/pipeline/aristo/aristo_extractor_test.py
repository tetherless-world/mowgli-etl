import os.path

from mowgli_etl.lib.etl.pipeline.aristo.aristo_extractor import AristoExtractor


def test_aristo_extractor(pipeline_storage):
    result = AristoExtractor().extract(force=False, storage=pipeline_storage)
    assert len(result) == 1
    file_path = result["combined_kb_tsv_file_path"]
    assert os.path.dirname(file_path) == str(pipeline_storage.extracted_data_dir_path)
    assert os.path.exists(file_path)
