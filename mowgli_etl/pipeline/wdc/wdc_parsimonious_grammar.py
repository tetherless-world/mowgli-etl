import json
import sys

from mowgli_etl.pipeline.wdc.wdc_product_dimensions import WdcProductDimensions
from mowgli_etl.pipeline.wdc.wdc_dimension_parser import WdcDimensionParser
from mowgli_etl.pipeline.wdc.wdc_offers_corpus_entry import WdcOffersCorpusEntry
from mowgli_etl.pipeline.wdc.wdc_constants import WDC_ARCHIVE_PATH

from parsimonious import Grammar

class WdcParsimoniousDimensionParser(WdcDimensionParser):
	def __init__(self):
		self.__GRAMMAR = Grammar(
						"""
						bin 			= (space* word* number*)*

						unit			= 'cm'/'in'/'ft'/'mm'/'m'
						dimensions 		= (dimension space*)+
						dimension 		= number+ space direction
						direction 		= 'h'/'w'/'d'/'l'
						number 			= ~'[0-9]+'
						words 			= word+
						word 			= ~'[A-z]*'
						space			= ~'\s'
						"""
						)

	def parse(self, *, entry: WdcOffersCorpusEntry):
		if entry.description is not None:
			description = self.__GRAMMAR.parse(entry.description)
			print(description)


if __name__=="__main__":
	with open(
	    WDC_ARCHIVE_PATH / "offers_corpus_english_v2_random_100_clean.jsonl", "r"
	) as data:
	    count = 0
	    for row in data:
	        count += 1
	        if count == 34:
	        	WdcParsimoniousDimensionParser().parse(entry=WdcOffersCorpusEntry.from_json(row))
