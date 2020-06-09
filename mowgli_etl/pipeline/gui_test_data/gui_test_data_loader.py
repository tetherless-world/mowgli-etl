from pathlib import Path

from mowgli_etl._edge_loader import _EdgeLoader
from mowgli_etl._node_loader import _NodeLoader
from mowgli_etl._path_loader import _PathLoader
from mowgli_etl.loader.cskg_csv.cskg_csv_edge_loader import CskgCsvEdgeLoader
from mowgli_etl.loader.cskg_csv.cskg_csv_node_loader import CskgCsvNodeLoader
from mowgli_etl.loader.json.json_edge_loader import JsonEdgeLoader
from mowgli_etl.loader.json.json_node_loader import JsonNodeLoader
from mowgli_etl.loader.json.jsonl_path_loader import JsonlPathLoader
from mowgli_etl.paths import PROJECT_ROOT
from mowgli_etl.loader.cskg_csv.cskg_csv_loader import CskgCsvLoader
from mowgli_etl.pipeline.gui_test_data.gui_test_data_pipeline import GuiTestDataPipeline
from mowgli_etl.pipeline_storage import PipelineStorage


class GuiTestDataLoader(_EdgeLoader, _NodeLoader, _PathLoader):
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

    def __init__(self):
        self.__edge_loaders = []
        self.__node_loaders = []
        self.__path_loaders = []

    def close(self):
        for loaders in (self.__edge_loaders, self.__node_loaders, self.__path_loaders):
            for loader in loaders:
                loader.close()

    def load_edge(self, edge):
        for loader in self.__edge_loaders:
            loader.load_edge(edge)

    def load_node(self, node):
        for loader in self.__node_loaders:
            loader.load_node(node)

    def load_path(self, path):
        for loader in self.__path_loaders:
            loader.load_path(path)

    def open(self, storage):
        from mowgli_etl.pipeline.gui_test_data.gui_test_data_pipeline import GuiTestDataPipeline
        scala_storage = PipelineStorage(pipeline_id=GuiTestDataPipeline.ID, root_data_dir_path=PROJECT_ROOT, loaded_data_dir_path=PROJECT_ROOT.parent / "mcs-portal" / "conf" / "test_data")
        ts_storage = PipelineStorage(pipeline_id=GuiTestDataPipeline.ID, root_data_dir_path=PROJECT_ROOT, loaded_data_dir_path=PROJECT_ROOT.parent / "mcs-portal" / "test" / "integration" / "cypress" / "fixtures")

        self.__edge_loaders.append(CskgCsvEdgeLoader(bzip=True).open(storage))
        self.__edge_loaders.append(JsonEdgeLoader().open(ts_storage))
        self.__node_loaders.append(CskgCsvNodeLoader(bzip=True).open(scala_storage))
        self.__node_loaders.append(JsonNodeLoader().open(ts_storage))
        self.__path_loaders.append(JsonlPathLoader().open(scala_storage))

        return self
