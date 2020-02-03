from mowgli.lib.etl._pipeline import _Pipeline
from mowgli.lib.etl.webchild.webchild_extractor import webchildExtractor
from mowgli.lib.etl.webchild.webchild_transformer import webchildTransformer


class webchildPipeline(_Pipeline):
    """
    ETL pipeline that extracts from the Small World of Words corpus.

    https://smallworldofwords.org
    """

    def __init__(self, *, webchild_csv_file_paths: list, **kwds):
        _Pipeline.__init__(
            self,
            extractor=webchildExtractor(webchild_csv_file_path=webchild_csv_file_paths),
            id="webchild",
            transformer=webchildTransformer(),
            **kwds
        )

    @classmethod
    def add_arguments(cls, arg_parser):
        arg_parser.add_argument("--webchild-csv-file-path", help="webchild .csv file paths", required=True)
