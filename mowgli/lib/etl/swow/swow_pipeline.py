from mowgli.lib.etl._pipeline import _Pipeline
from mowgli.lib.etl.swow.swow_extractor import SwowExtractor
from mowgli.lib.etl.swow.swow_transformer import SwowTransformer


class SwowPipeline(_Pipeline):
    """
    ETL pipeline that extracts from the Small World of Words corpus.

    https://smallworldofwords.org
    """

    def __init__(self, *, csv_file_path: str, **kwds):
        _Pipeline.__init__(
            self,
            extractor=SwowExtractor(csv_file_path=csv_file_path),
            id="swow",
            transformer=SwowTransformer(),
            **kwds
        )

    @classmethod
    def add_arguments(cls, arg_parser):
        arg_parser.add_argument("--csv-file-path", help="SWOW strength .csv file path", required=True)
