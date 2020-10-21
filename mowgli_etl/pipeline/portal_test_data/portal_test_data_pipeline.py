from mowgli_etl._pipeline import _Pipeline


class PortalTestDataPipeline(_Pipeline):
    ID = "P0"

    def __init__(self, loader: str, **kwds):
        from mowgli_etl.pipeline.portal_test_data.portal_test_data_extractor import (
            PortalTestDataExtractor,
        )
        from mowgli_etl.pipeline.portal_test_data.portal_test_data_loader import (
            PortalTestDataLoader,
        )
        from mowgli_etl.pipeline.portal_test_data.portal_test_data_transformer import (
            PortalTestDataTransformer,
        )

        _Pipeline.__init__(
            self,
            extractor=PortalTestDataExtractor(),
            id=self.ID,
            loader=PortalTestDataLoader(),
            transformer=PortalTestDataTransformer(),
            **kwds
        )
