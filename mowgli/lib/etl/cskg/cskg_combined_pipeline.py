from os import PathLike
from pathlib import PurePath
from typing import Tuple, Union

from mowgli.lib.etl._pipeline import _Pipeline
from mowgli.lib.etl.cskg.cskg_csv_transformer import CskgCsvTransformer
from mowgli.lib.etl.cskg.cskg_pipeline_extractor import CskgPipelineExtractor


class CskgCombinedPipeline(_Pipeline):
    def __init__(self, *, id: str, pipelines: Tuple[_Pipeline, ...], root_data_dir_path: Union[str, PathLike, PurePath]):
        super().__init__(
            id=id,
            extractor=CskgPipelineExtractor(root_data_dir_path=root_data_dir_path, pipelines=pipelines),
            transformer=CskgCsvTransformer()
        )
