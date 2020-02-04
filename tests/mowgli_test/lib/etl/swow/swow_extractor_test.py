<<<<<<< HEAD
from mowgli.lib.etl.swow.swow_extractor import SwowExtractor

def test_swow_extractor():
    file_path = '/test/file/path'
    extractor = SwowExtractor(csv_file_path=file_path)
    expected_extraction = {'csv_file_path': file_path}
    assert extractor.extract() == expected_extraction
=======
from mowgli.lib.etl.swow.swow_constants import STRENGTH_FILE_KEY
from mowgli.lib.etl.swow.swow_extractor import SwowExtractor

def test_swow_extractor(pipeline_storage, sample_swow_strengths, sample_archive_path):
    extractor = SwowExtractor(swow_archive_path=sample_archive_path)
    extraction = extractor.extract(force=False, storage=pipeline_storage)
    contents = extraction[STRENGTH_FILE_KEY].read()
    expected_contents = sample_swow_strengths.read()
    assert contents == expected_contents
    
>>>>>>> f528e6b5c73c4cc8f9bf8dff32ab4079085d3fde
