import os.path

from mowgli.lib.etl.pipeline.has_part.has_part_extractor import HasPartExtractor


def test_has_part_extractor(pipeline_storage):
    result = HasPartExtractor().extract(force=False, storage=pipeline_storage)
    assert len(result) == 1
    file_path = result["has_part_kb_jsonl_file_path"]
    assert os.path.dirname(file_path) == str(pipeline_storage.extracted_data_dir_path)
    assert os.path.exists(file_path)
