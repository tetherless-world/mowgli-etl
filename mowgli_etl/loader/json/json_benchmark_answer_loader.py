from mowgli_etl.loader._benchmark_answer_loader import _BenchmarkAnswerLoader
from mowgli_etl.loader.json._json_loader import _JsonLoader


class JsonBenchmarkAnswerLoader(_BenchmarkAnswerLoader, _JsonLoader):
    _JSON_FILE_NAME = "benchmark_answers.json"
    close = _JsonLoader.close
    load_benchmark_answer = _JsonLoader._load_model
    open = _JsonLoader.open
