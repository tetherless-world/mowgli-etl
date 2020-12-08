from mowgli_etl.pipeline.wdc.wdc_offers_corpus import WdcOffersCorpus
from mowgli_etl.pipeline.wdc.wdc_constants import WDC_ARCHIVE_PATH
from mowgli_etl.pipeline.wdc.parsimonious_parser.wdc_parsimonious_dimension_parser import WdcParsimoniousDimensionParser as WPDP
import dataclasses

if __name__ == "__main__":
	min_vals = dict()
	max_vals = dict()
	corpus = WdcOffersCorpus(wdc_json_file_path = WDC_ARCHIVE_PATH / "offers_corpus_english_v2_1000.jsonl")
	dim_classifier = WPDP()
	for entry in corpus.entries():
		dimensions = dim_classifier.parse(entry=entry)
		for dimension in dimensions:
			dimension = dimension.dimensions.to_english()
			for field in dataclasses.fields(dimension):
				dim = getattr(dimension, field.name)
				if not dim:
					continue
				if field.name not in min_vals:
					min_vals[field.name] = dim.value
				else:
					min_vals[field.name] = min(min_vals[field.name], dim.value)
				if field.name not in max_vals:
					max_vals[field.name] = dim.value
				else:
					max_vals[field.name] = max(min_vals[field.name], dim.value)

	print("MINIMUM VALUES:\n")
	for key in sorted(list(min_vals.keys())):
		print(f"\t{key:<10}: {min_vals[key]}")

	print("\nMAXIMUM VALUES:\n")
	for key in sorted(list(max_vals.keys())):
		print(f"\t{key:<10}: {max_vals[key]}")


