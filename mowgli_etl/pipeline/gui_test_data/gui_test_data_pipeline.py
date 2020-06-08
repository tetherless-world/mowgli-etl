from mowgli_etl._pipeline import _Pipeline


class GuiTestDataPipeline(_Pipeline):
    ID = "gui_test_data"

    def __init__(self, loader: str, **kwds):
        from mowgli_etl.pipeline.gui_test_data.gui_test_data_extractor import GuiTestDataExtractor
        from mowgli_etl.pipeline.gui_test_data.gui_test_data_loader import GuiTestDataLoader
        from mowgli_etl.pipeline.gui_test_data.gui_test_data_transformer import GuiTestDataTransformer
        _Pipeline.__init__(
            self,
            extractor=GuiTestDataExtractor(),
            id=self.ID,
            loader=GuiTestDataLoader(),
            transformer=GuiTestDataTransformer(),
            **kwds
        )
