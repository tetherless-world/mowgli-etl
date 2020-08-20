import wdc_transformer
from pathlib import Path
from wdc_constants import WDC_ARCHIVE_PATH

for edge in WDCTransformer.transform(wdc_jsonl_file_path = WDC_ARCHIVE_PATH/"offers_corpus_english_v2_random_100.jsonl"):
	print(edge.id)
