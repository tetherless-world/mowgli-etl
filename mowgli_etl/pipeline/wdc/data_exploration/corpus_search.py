from mowgli_etl.pipeline.wdc.parsimonious_parser.wdc_parsimonious_dimension_parser import (
    WdcParsimoniousDimensionParser,
)
from mowgli_etl.pipeline.wdc.wdc_product_dimensions import WdcProductDimensions
from mowgli_etl.pipeline.wdc.wdc_offers_corpus_entry import WdcOffersCorpusEntry
from mowgli_etl.pipeline.wdc.wdc_offers_corpus import WdcOffersCorpus
from mowgli_etl.pipeline.wdc.wdc_constants import WDC_ARCHIVE_PATH

for count, entry in enumerate(WdcOffersCorpus(wdc_json_file_path = WDC_ARCHIVE_PATH / "offers_corpus_english_v2_1000.jsonl").entries()):
	
	parsed = WdcParsimoniousDimensionParser().parse(entry=entry)
	if len(parsed) > 0:
		print(count, parsed[0])
