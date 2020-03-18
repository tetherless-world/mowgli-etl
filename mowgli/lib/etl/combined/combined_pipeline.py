from typing import Tuple, Optional

from mowgli.lib.etl._pipeline import _Pipeline
from mowgli.lib.etl.combined.combined_pipeline_extractor import CombinedPipelineExtractor
from mowgli.lib.etl.cskg.cskg_csv_transformer import CskgCsvTransformer
from mowgli.lib.etl.eat.eat_pipeline import EatPipeline
from mowgli.lib.etl.swow.swow_pipeline import SwowPipeline
from mowgli.lib.etl.usf.usf_pipeline import UsfPipeline
from tests.mowgli_test.lib.etl.has_part.has_part_pipeline import HasPartPipeline


class CombinedPipeline(_Pipeline):
    def __init__(self, *, pipelines: Optional[Tuple[_Pipeline, ...]] = None, **kwargs):
        if pipelines is None:
            pipelines = self.__default_pipelines()
        super().__init__(
            id='combined',
            extractor=CombinedPipelineExtractor(pipelines=pipelines),
            transformer=CskgCsvTransformer()
        )

    def __default_pipelines(self) -> Tuple[_Pipeline, ...]:
        return (
            EatPipeline(),
            HasPartPipeline(),
            SwowPipeline(),
            UsfPipeline()
        )
