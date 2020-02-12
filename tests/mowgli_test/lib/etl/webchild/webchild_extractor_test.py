from mowgli.lib.etl.webchild.webchild_extractor import WebchildExtractor
import os

def test_webchild_extractor():
    fileDir = os.getcwd()+ r'\tests\mowgli_test\lib\etl\webchild'
    file_list = os.listdir(fileDir)
    txt_list = []
    for file in file_list:
        print(file[-3:])
        if file[-3:] == "txt":
            txt_list.append(file)
    print(txt_list)
    extractor = WebchildExtractor(csv_file_paths = txt_list)
    expected_extraction = {'csv_file_paths': ['test_webchild_partof_memberof.txt','test_webchild_partof_physical.txt','test_webchild_partof_substanceof.txt', 'test_WordNetWrapper.txt']}
    assert extractor.extract() == expected_extraction
