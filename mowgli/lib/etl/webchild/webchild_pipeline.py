from mowgli.lib.etl._pipeline import _Pipeline
from mowgli.lib.etl.webchild.webchild_extractor import WebchildExtractor
from mowgli.lib.etl.webchild.webchild_transformer import WebchildTransformer
import os
import pathlib

class WebchildPipeline(_Pipeline):

    def __init__(self, *, memberof_csv_file_path: str, physical_csv_file_path: str, substanceof_csv_file_path: str, wordnet_csv_file_path: str, **kwds):
        _Pipeline.__init__(
            self,
            extractor= WebchildExtractor(memberof_csv_file_path=memberof_csv_file_path, physical_csv_file_path=physical_csv_file_path, substanceof_csv_file_path=substanceof_csv_file_path, wordnet_csv_file_path=wordnet_csv_file_path),
            id="webchild",
            transformer=WebchildTransformer(),
            **kwds
        )
 
    @classmethod
    def add_arguments(cls, arg_parser):
        path_dir = pathlib.Path(__file__).parent.absolute().parents[3]
        arg_parser.add_argument("--memberof-csv-file-path", help="WebChild memberof .csv file path", required=False, default =path_dir.joinpath('data\webchild\webchild_partof_memberof.txt'))
        arg_parser.add_argument("--physical-csv-file-path", help="WebChild physical .csv file path", required=False, default = path_dir.joinpath('data\webchild\webchild_partof_physical.txt'))
        arg_parser.add_argument("--substanceof-csv-file-path", help="WebChild substance of .csv file path", required=False, default = path_dir.joinpath('data/webchild\webchild_partof_substanceof.txt'))
        arg_parser.add_argument("--wordnet-csv-file-path", help="WebChild WordNet .csv file path", required=False, default = path_dir.joinpath('data\webchild\WordNetWrapper.txt'))



