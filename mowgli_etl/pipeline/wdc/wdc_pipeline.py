from mowgli_etl._pipeline import _Pipeline
from mowgli_etl.pipeline.wdc.wdc_constants import WDC_ARCHIVE_PATH
from mowgli_etl.pipeline.wdc.wdc_extractor import WdcExtractor
from mowgli_etl.pipeline.wdc.wdc_transformer import WdcTransformer

class WdcPipeline(_Pipeline):
	"""
	ETL pipeline that extracts from the Web Data Commons corpus.

	https://webdatacommons.org
	"""

	def __init__(self, *, wdc_archive_path: str = WDC_ARCHIVE_PATH, **kwds):
		_Pipeline.__init__(
			self,
			extractor=WdcExtractor(wdc_archive_path=wdc_archive_path),
			id="wdc",
			transformer=WdcTransformer(),
			**kwds
		)

	@classmethod
	def add_arguments(cls, arg_parser):
		_Pipeline.add_arguments(arg_parser)
		arg_parser.add_arguments(
			"--wdc-archive-path",
			help="ath to a bz2 archive to use as a source of WDC data",
			required=False,
			default=WDC_ARCHIVE_PATH)
