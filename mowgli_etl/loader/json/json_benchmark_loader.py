from mowgli_etl.loader._benchmark_loader import _BenchmarkLoader
from mowgli_etl.loader.json._json_loader import _JsonLoader


class JsonBenchmarkLoader(_BenchmarkLoader, _JsonLoader):
    def __init__(self):
        _BenchmarkLoader.__init__(self)
        _JsonLoader.__init__(self, json_file_name="benchmarks.json")

    def load_benchmark(self, benchmark):
        self._load_model(benchmark)
