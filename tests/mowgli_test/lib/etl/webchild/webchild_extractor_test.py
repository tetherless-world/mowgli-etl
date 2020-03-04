from mowgli.lib.etl.webchild.webchild_extractor import WebchildExtractor
import os
import pathlib
from mowgli.paths import PROJECT_ROOT

def test_webchild_extractor(pipeline_storage):
    path_dir = PROJECT_ROOT.joinpath("tests","mowgli_test","lib","etl","webchild")
    os.chdir(path_dir) 

    extractor = WebchildExtractor(memberof_csv_file_path = path_dir.joinpath('test_webchild_partof_memberof.txt'),
                                  physical_csv_file_path= path_dir.joinpath('test_webchild_partof_physical.zip'), 
                                  substanceof_csv_file_path= path_dir.joinpath('test_webchild_partof_substanceof.txt'), 
                                  wordnet_csv_file_path= path_dir.joinpath('test_WordNetWrapper.txt' ))
    
    expected_extraction = { "memberof_csv_file_path": 'test_webchild_partof_memberof.txt',
                            "physical_csv_file_path": 'test_webchild_partof_physical.txt',
                            "substanceof_csv_file_path": 'test_webchild_partof_substanceof.txt',
                            "wordnet_csv_file_path": 'test_WordNetWrapper.txt'}


    real_extraction = extractor.extract()

    

    for key in real_extraction:
        real_extraction[key] = os.path.basename(os.path.normpath(real_extraction[key]))
    
    
    assert  real_extraction== expected_extraction
