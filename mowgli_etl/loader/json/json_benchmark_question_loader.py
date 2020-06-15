from mowgli_etl.loader._benchmark_loader import _BenchmarkLoader
from mowgli_etl.loader._benchmark_question_loader import _BenchmarkQuestionLoader
from mowgli_etl.loader.json._json_loader import _JsonLoader


class JsonBenchmarkQuestionLoader(_BenchmarkQuestionLoader, _JsonLoader):
    _JSON_FILE_NAME = "benchmark_questions.json"
    close = _JsonLoader.close
    load_benchmark_question = _JsonLoader._load_model
    open = _JsonLoader.open
