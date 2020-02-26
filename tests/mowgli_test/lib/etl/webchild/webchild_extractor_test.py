from mowgli.lib.etl.webchild.webchild_extractor import WebchildExtractor
import os
import pathlib

def test_webchild_extractor():
    path_dir = str(pathlib.Path(__file__).parent.absolute()) 
    
    extractor = WebchildExtractor(memberof_csv_file_path = path_dir + r'\test_webchild_partof_memberof.txt', 
                                  physical_csv_file_path= path_dir + r'\test_webchild_partof_physical.txt', 
                                  substanceof_csv_file_path= path_dir + r'\test_webchild_partof_substanceof.txt', 
                                  wordnet_csv_file_path= path_dir + r'\test_WordNetWrapper.txt' )
    
    expected_extraction = { "memberof_csv_file_path": 'test_webchild_partof_memberof.txt',
                            "physical_csv_file_path": 'test_webchild_partof_physical.txt',
                            "substanceof_csv_file_path": 'test_webchild_partof_substanceof.txt',
                            "wordnet_csv_file_path": 'test_WordNetWrapper.txt'}

    
    real_extraction = extractor.extract()

    for key in real_extraction:
        real_extraction[key] = os.path.basename(os.path.normpath(real_extraction[key]))
    
    
    assert  real_extraction== expected_extraction
