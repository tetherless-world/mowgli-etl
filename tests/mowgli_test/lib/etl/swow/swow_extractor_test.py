from mowgli.lib.etl.swow.swow_extractor import SwowExtractor

def test_swow_extractor():
    file_path = '/test/file/path'
    extractor = SwowExtractor(csv_file_path=file_path)
    expected_extraction = {'csv_file_path': file_path}
    assert extractor.extract() == expected_extraction
