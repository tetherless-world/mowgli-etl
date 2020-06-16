from mowgli_etl.loader._benchmark_loader import _BenchmarkLoader
from mowgli_etl.loader.json._json_loader import _JsonLoader


class JsonBenchmarkLoader(_BenchmarkLoader, _JsonLoader):
    _JSON_FILE_NAME = "benchmarks.json"
    close = _JsonLoader.close
    load_benchmark = _JsonLoader._load_model
    open = _JsonLoader.open
