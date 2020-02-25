from _pipeline import _Pipeline
from mowgli.lib.webchild.webchild_extractor import webchildExtractor
from mowgli.lib.webchild.webchild_transformer import webchildTransformer
import os


class WebchildPipeline(_Pipeline):

    def __init__(self, *, memberof_csv_file_path: str, physical_csv_file_path: str, substanceof_csv_file_path: str, wordnet_csv_file_path: str, **kwds):
        _Pipeline.__init__(
            self,
            extractor= webChildExtractor(memberof_csv_file_path=memberof_csv_file_path, physical_csv_file_path=physical_csv_file_path, substanceof_csv_file_path=substanceof_csv_file_path, wordnet_csv_file_path=wordnet_csv_file_path),
            id="webchild",
            transformer=webchildTransformer(),
            **kwds
        )
 
       @classmethod
    def add_arguments(cls, arg_parser):
        arg_parser.add_argument("--memberOf-csv-file-path", help="WebChild memberof .csv file path", required=True, default = '../../../../Data/WebChildData/memberof.txt')
        arg_parser.add_argument("--physical-csv-file-path", help="WebChild physical .csv file path", required=True, default = '../../../../Data/WebChildData/webchild_partof_physical.txt')
        arg_parser.add_argument("--substance-csv-file-path", help="WebChild substance of .csv file path", required=True, default = '../../../../Data/WebChildData/webchild_partof_substanceof.txt')
        arg_parser.add_argument("--WorddNet-csv-file-path", help="WebChild WordNet .csv file path", required=True, default = '../../../../Data/WebChildData/WordNetWrapper.txt')

