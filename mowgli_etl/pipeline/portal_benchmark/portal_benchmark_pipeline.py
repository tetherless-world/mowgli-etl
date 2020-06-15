from mowgli_etl._pipeline import _Pipeline


class PortalBenchmarkPipeline(_Pipeline):
    ID = "portal_benchmark"

    def __init__(self, loader: str, **kwds):
        from mowgli_etl.pipeline.portal_benchmark.portal_benchmark_extractor import PortalBenchmarkExtractor
        from mowgli_etl.pipeline.portal_benchmark.portal_benchmark_loader import PortalBenchmarkLoader
        from mowgli_etl.pipeline.portal_benchmark.portal_benchmark_transformer import PortalBenchmarkTransformer
        _Pipeline.__init__(
            self,
            extractor=PortalBenchmarkExtractor(),
            id=self.ID,
            loader=PortalBenchmarkLoader(),
            transformer=PortalBenchmarkTransformer(),
            **kwds
        )
