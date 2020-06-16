from mowgli_etl.loader._benchmark_submission_loader import _BenchmarkSubmissionLoader
from mowgli_etl.loader.json._json_loader import _JsonLoader


class JsonBenchmarkSubmissionLoader(_BenchmarkSubmissionLoader, _JsonLoader):
    _JSON_FILE_NAME = "benchmark_submissions.json"
    close = _JsonLoader.close
    load_benchmark_submission = _JsonLoader._load_model
    open = _JsonLoader.open
