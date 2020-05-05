from typing import Tuple, Optional

from configargparse import ArgParser

from mowgli.lib.etl._pipeline import _Pipeline
from mowgli.lib.etl.pipeline.combined.combined_pipeline_extractor import CombinedPipelineExtractor
from mowgli.lib.etl.pipeline.cskg.cskg_csv_transformer import CskgCsvTransformer


class CombinedPipeline(_Pipeline):
    def __init__(self, *, pipelines: Optional[Tuple[_Pipeline, ...]] = None, serial: Optional[bool], **kwds):
        if pipelines is None:
            pipelines = self.__default_pipelines()
        super().__init__(
            id="combined",
            extractor=CombinedPipelineExtractor(pipelines=pipelines, parallel=not bool(serial)),
            transformer=CskgCsvTransformer(),
            **kwds
        )

    @classmethod
    def add_arguments(cls, arg_parser: ArgParser) -> None:
        _Pipeline.add_arguments(arg_parser)
        arg_parser.add_argument("--serial", action="store_true", help="run serially, for testing")

    def __default_pipelines(self) -> Tuple[_Pipeline, ...]:
        # Import these here instead of above so that CombinedPipeline is the only _Pipeline subclass at the top level of the module.
        # The pipeline module loader relies on that.
        from mowgli.lib.etl.pipeline.aristo.aristo_pipeline import AristoPipeline
        from mowgli.lib.etl.pipeline.eat.eat_pipeline import EatPipeline
        from mowgli.lib.etl.pipeline.food_on.food_on_pipeline import FoodOnPipeline
        from mowgli.lib.etl.pipeline.has_part.has_part_pipeline import HasPartPipeline
        from mowgli.lib.etl.pipeline.swow.swow_pipeline import SwowPipeline
        from mowgli.lib.etl.pipeline.usf.usf_pipeline import UsfPipeline
        from mowgli.lib.etl.pipeline.web_child.web_child_pipeline import WebChildPipeline

        return (
            AristoPipeline(),
            EatPipeline(),
            FoodOnPipeline(),
            HasPartPipeline(),
            SwowPipeline(),
            UsfPipeline(),
            WebChildPipeline(),
        )
