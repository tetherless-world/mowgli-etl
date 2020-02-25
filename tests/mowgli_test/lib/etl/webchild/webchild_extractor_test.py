from mowgli.lib.etl.webchild.webchild_extractor import WebchildExtractor
import os
import pathlib

def test_webchild_extractor():
    path_dir = str(pathlib.Path(__file__).parent.absolute()) 
    
    extractor = WebchildExtractor(memberof_csv_file_path = path_dir + r'\test_webchild_partof_memberof.txt', 
                                  physical_csv_file_path= path_dir + r'\test_webchild_partof_physical.txt', 
                                  substanceof_csv_file_path= path_dir + r'\test_webchild_partof_substanceof.txt', 
                                  wordnet_csv_file_path= path_dir + r'\test_WordNetWrapper.txt' )
    
    expected_extraction = {'csv_file_paths': ['test_webchild_partof_memberof.txt',
                                              'test_webchild_partof_physical.txt',
                                              'test_webchild_partof_substanceof.txt',
                                              'test_WordNetWrapper.txt']}
    real_extraction = extractor.extract()

    for i in range(0,len(real_extraction['csv_file_paths'])):
        real_extraction['csv_file_paths'][i] = os.path.basename(os.path.normpath(expected_extraction['csv_file_paths'][i]))
    
    real_extraction['csv_file_paths'].sort()
    expected_extraction['csv_file_paths'].sort() 
    
    assert  real_extraction== expected_extraction
