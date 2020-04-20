from mowgli.lib.etl.swow.swow_constants import SWOW_CSV_FILE_KEY
from mowgli.lib.etl.swow.swow_extractor import SwowExtractor


def test_swow_extractor(pipeline_storage, sample_swow_csv_path, sample_archive_path):
    extractor = SwowExtractor(swow_archive_path=sample_archive_path)
    extraction = extractor.extract(force=False, storage=pipeline_storage)
    with open(extraction[SWOW_CSV_FILE_KEY], mode='r') as extracted_strengths_file:
        contents = extracted_strengths_file.read()
    with open(sample_swow_csv_path, mode='r') as sample_strengths_file:
        expected_contents = sample_strengths_file.read()

    assert contents == expected_contents
