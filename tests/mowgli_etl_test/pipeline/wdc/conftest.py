import pytest

from mowgli_etl.pipeline.wdc.wdc_constants import WDC_ARCHIVE_PATH
from mowgli_etl.pipeline.wdc.wdc_offers_corpus import WdcOffersCorpus

@pytest.fixture
def wdc_large_offers_corpus():
	return WdcOffersCorpus(wdc_json_file_path = WDC_ARCHIVE_PATH / "offers_corpus_english_v2_1000.jsonl")
