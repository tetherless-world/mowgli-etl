import os.path

from mowgli.lib.etl.has_part.has_part_extractor import HasPartExtractor


def test_has_part_extractor(pipeline_storage):
    result = HasPartExtractor().extract(force=False, storage=pipeline_storage)
    assert len(result) == 1
    file_path = result["has_part_kb_jsonl_bz2_file_path"]
    assert file_path == HasPartExtractor.HAS_PART_KB_JSONL_BZ2_FILE_PATH
    assert os.path.exists(file_path)
