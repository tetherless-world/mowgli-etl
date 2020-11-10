import pytest

from mowgli_etl.pipeline.wdc.wdc_constants import WDC_ARCHIVE_PATH

@pytest.fixture
def wdc_large_json_file_path():
    return WDC_ARCHIVE_PATH / "offers_corpus_english_v2_1000.jsonl"
