from mowgli_etl.loader._benchmark_loader import _BenchmarkLoader
from mowgli_etl.loader._path_loader import _PathLoader
from mowgli_etl.loader.json._jsonl_loader import _JsonlLoader


class JsonlBenchmarkLoader(_BenchmarkLoader, _JsonlLoader):
    _JSONL_FILE_NAME = "benchmarks.jsonl"
    close = _JsonlLoader.close
    load_benchmark = _JsonlLoader._load_model
    open = _JsonlLoader.open
