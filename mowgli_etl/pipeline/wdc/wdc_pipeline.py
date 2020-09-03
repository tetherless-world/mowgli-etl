from mowgli_etl._pipeline import _Pipeline
from mowgli_etl.pipeline.wdc.wdc_constants import WDC_ARCHIVE_PATH, WDC_DATASOURCE_ID
from mowgli_etl.pipeline.wdc.wdc_extractor import WdcExtractor
from mowgli_etl.pipeline.wdc.wdc_transformer import WdcTransformer

class WdcPipeline(_Pipeline):
    """
    ETL pipeline that extracts from the Web Data Commons corpus.

    https://webdatacommons.org
    """

    def __init__(self, **kwds):
        _Pipeline.__init__(
            self,
            extractor=WdcExtractor(),
            id=WDC_DATASOURCE_ID,
            transformer=WdcTransformer(),
            **kwds
        )
