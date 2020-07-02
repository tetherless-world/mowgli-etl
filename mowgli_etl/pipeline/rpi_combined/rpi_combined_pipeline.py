from typing import Tuple, Optional

from configargparse import ArgParser

from mowgli_etl._pipeline import _Pipeline
from mowgli_etl.pipeline.cskg_csv.cskg_csv_transformer import CskgCsvTransformer
from mowgli_etl.pipeline.rpi_combined.rpi_combined_extractor import RpiCombinedExtractor


class RpiCombinedPipeline(_Pipeline):
    def __init__(self, *, pipelines: Optional[Tuple[_Pipeline, ...]] = None, parallel: Optional[bool], **kwds):
        if pipelines is None:
            pipelines = self.__default_pipelines()
        super().__init__(
            id="combined",
            extractor=RpiCombinedExtractor(pipelines=pipelines, parallel=bool(parallel)),
            single_datasource=False,
            transformer=CskgCsvTransformer(),
            **kwds
        )

    @classmethod
    def add_arguments(cls, arg_parser: ArgParser) -> None:
        _Pipeline.add_arguments(arg_parser)
        arg_parser.add_argument("--parallel", action="store_true", help="run pipelines in parallel")

    def __default_pipelines(self) -> Tuple[_Pipeline, ...]:
        # Import these here instead of above so that RpiCombinedPipeline is the only _Pipeline subclass at the top level of the module.
        # The pipeline module loader relies on that.
        from mowgli_etl.pipeline.aristo.aristo_pipeline import AristoPipeline
        from mowgli_etl.pipeline.eat.eat_pipeline import EatPipeline
        from mowgli_etl.pipeline.food_on.food_on_pipeline import FoodOnPipeline
        from mowgli_etl.pipeline.has_part.has_part_pipeline import HasPartPipeline
        from mowgli_etl.pipeline.sentic.sentic_pipeline import SenticPipeline
        from mowgli_etl.pipeline.swow.swow_pipeline import SwowPipeline
        from mowgli_etl.pipeline.usf.usf_pipeline import UsfPipeline
        # from mowgli_etl.pipeline.web_child.web_child_pipeline import WebChildPipeline

        return (
            AristoPipeline(),
            EatPipeline(),
            FoodOnPipeline(),
            HasPartPipeline(),
            SenticPipeline(),
            SwowPipeline(),
            UsfPipeline(),
            # WebChildPipeline(),  # Takes a long time to run and produces dubious triples
        )
