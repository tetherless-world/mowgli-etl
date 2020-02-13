from mowgli.lib.etl.webchild.webchild_extractor import WebchildExtractor
import os
import pathlib

def test_webchild_extractor():
    fileDir = pathlib.Path(__file__).parent.absolute()
    file_list = os.listdir(fileDir)
    txt_list = []
    for file in file_list:
        if file[-3:] == "txt":
            txt_list.append(file)
    extractor = WebchildExtractor(csv_file_paths = txt_list)
    expected_extraction = {'csv_file_paths': ['test_webchild_partof_substanceof.txt', 'test_webchild_partof_memberof.txt', 'test_webchild_partof_physical.txt', 'test_WordNetWrapper.txt']}
    assert extractor.extract() == expected_extraction
