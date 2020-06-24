from mowgli_etl._pipeline import _Pipeline


class McsBenchmarkPipeline(_Pipeline):
    ID = "mcs_benchmark"

    def __init__(self, bzip: bool = True, **kwargs):
        from mowgli_etl.pipeline.mcs_benchmark.mcs_benchmark_extractor import (
            McsBenchmarkExtractor,
        )
        from mowgli_etl.pipeline.mcs_benchmark.mcs_benchmark_loader import (
            McsBenchmarkLoader,
        )
        from mowgli_etl.pipeline.mcs_benchmark.mcs_benchmark_transformer import (
            McsBenchmarkTransformer,
        )

        _Pipeline.__init__(
            self,
            extractor=McsBenchmarkExtractor(),
            id=self.ID,
            loader=McsBenchmarkLoader(bzip=bzip),
            transformer=McsBenchmarkTransformer(),
        )
