from mowgli_etl.pipeline.wdc.data_exploration.offers_corpus_english_v2_random_sample import data_sample
from pathlib import Path

import warnings
warnings.simplefilter(action='ignore', category=StopIteration)

def test_100_data_sample(wdc_large_json_file_path: Path):
	count = 0
	for entry in data_sample(wdc_large_json_file_path, 100):
		count += 1
	assert count == 100

def test_small_data_sample(wdc_large_json_file_path: Path):
	for item in data_sample(wdc_large_json_file_path, 0):
		assert item is None

def test_massive_data_sample(wdc_large_json_file_path: Path):
	for item in data_sample(wdc_large_json_file_path, 10**8):
		assert item is None
