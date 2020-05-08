from mowgli_etl.lib.etl._pipeline import _Pipeline
from mowgli_etl.lib.etl.pipeline.swow.swow_constants import SWOW_ARCHIVE_PATH
from mowgli_etl.lib.etl.pipeline.swow.swow_extractor import SwowExtractor
from mowgli_etl.lib.etl.pipeline.swow.swow_transformer import SwowTransformer


class SwowPipeline(_Pipeline):
    """
    ETL pipeline that extracts from the Small World of Words corpus.

    https://smallworldofwords.org
    """

    def __init__(self, *, swow_archive_path: str = SWOW_ARCHIVE_PATH, **kwds):
        _Pipeline.__init__(
            self,
            extractor=SwowExtractor(swow_archive_path=swow_archive_path),
            id="swow",
            transformer=SwowTransformer(),
            **kwds
        )

    @classmethod
    def add_arguments(cls, arg_parser):
        _Pipeline.add_arguments(arg_parser)
        arg_parser.add_argument(
            "--swow-archive-path",
            help="Path to a bz2 archive to use as a source of SWOW data",
            required=False,
            default=SWOW_ARCHIVE_PATH)
