from pathlib import Path

from mowgli_etl.loader.json.jsonl_path_loader import JsonlPathLoader
from mowgli_etl.paths import PROJECT_ROOT
from mowgli_etl.loader.cskg_csv.cskg_csv_loader import CskgCsvLoader
from mowgli_etl.pipeline.gui_test_data.gui_test_data_pipeline import GuiTestDataPipeline
from mowgli_etl.pipeline_storage import PipelineStorage


class GuiTestDataLoader(CskgCsvLoader, JsonlPathLoader):
    class __CustomPipelineStorage(PipelineStorage):
        LOADED_DATA_DIR_PATH = PROJECT_ROOT.parent / "mcs-portal" / "conf" / "test_data"
        assert LOADED_DATA_DIR_PATH.exists(), LOADED_DATA_DIR_PATH

        def __init__(self, *, pipeline_id: str, root_data_dir_path: Path):
            PipelineStorage.__init__(
                self,
                pipeline_id=pipeline_id,
                loaded_data_dir_path=self.LOADED_DATA_DIR_PATH,
                root_data_dir_path=root_data_dir_path
            )

    def close(self):
        CskgCsvLoader.close(self)
        JsonlPathLoader.close(self)

    def open(self, storage):
        # Ignore PipelineStorage passed in, write to the GUI test data directory
        storage = self.__CustomPipelineStorage(pipeline_id=GuiTestDataPipeline.ID, root_data_dir_path=storage.root_data_dir_path)
        CskgCsvLoader.open(self, storage)
        JsonlPathLoader.open(self, storage)
        return self
