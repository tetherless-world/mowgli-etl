from mowgli_etl.pipeline.wdc.wdc_offers_corpus import WdcOffersCorpus
from pathlib import Path

import warnings
warnings.simplefilter(action='ignore', category=StopIteration)

def test_100_data_sample(wdc_large_offers_corpus: WdcOffersCorpus):
	count = 0
	for entry in wdc_large_offers_corpus.sample(100):
		count += 1
	assert count == 100

def test_small_data_sample(wdc_large_offers_corpus: WdcOffersCorpus):
	for item in wdc_large_offers_corpus.sample(0):
		assert item is None

def test_massive_data_sample(wdc_large_offers_corpus: WdcOffersCorpus):
	for item in wdc_large_offers_corpus.sample(10**8):
		assert item is None
