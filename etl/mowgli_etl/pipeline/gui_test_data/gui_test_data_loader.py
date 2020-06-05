from pathlib import Path

from mowgli_etl.paths import PROJECT_ROOT
from mowgli_etl.pipeline.cskg_csv.cskg_csv_loader import CskgCsvLoader
from mowgli_etl.pipeline.gui_test_data.gui_test_data_pipeline import GuiTestDataPipeline
from mowgli_etl.pipeline_storage import PipelineStorage


class GuiTestDataLoader(CskgCsvLoader):
    class __CustomPipelineStorage(PipelineStorage):
        def __init__(self, *, pipeline_id: str, root_data_dir_path: Path):
            PipelineStorage.__init__(
                self,
                pipeline_id=pipeline_id,
                loaded_data_dir_path=PROJECT_ROOT.parent / "gui" / "conf" / "test_data",
                root_data_dir_path=root_data_dir_path
            )

    def open(self, storage):
        # Ignore PipelineStorage passed in, write to the GUI test data directory
        return \
            CskgCsvLoader.open(
                self,
                self.__CustomPipelineStorage(pipeline_id=GuiTestDataPipeline.ID, root_data_dir_path=storage.root_data_dir_path)
            )
