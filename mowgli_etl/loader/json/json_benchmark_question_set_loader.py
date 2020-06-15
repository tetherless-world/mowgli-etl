from mowgli_etl.loader._benchmark_loader import _BenchmarkLoader
from mowgli_etl.loader._benchmark_question_loader import _BenchmarkQuestionLoader
from mowgli_etl.loader._benchmark_question_set_loader import _BenchmarkQuestionSetLoader
from mowgli_etl.loader.json._json_loader import _JsonLoader


class JsonBenchmarkQuestionSetLoader(_BenchmarkQuestionSetLoader, _JsonLoader):
    _JSON_FILE_NAME = "benchmark_question_sets.json"
    close = _JsonLoader.close
    load_benchmark_question_set = _JsonLoader._load_model
    open = _JsonLoader.open
