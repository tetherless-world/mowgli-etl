from mowgli_etl.loader._benchmark_question_set_loader import _BenchmarkQuestionSetLoader
from mowgli_etl.loader.json._jsonl_loader import _JsonlLoader


class JsonlBenchmarkQuestionSetLoader(_BenchmarkQuestionSetLoader, _JsonlLoader):
    _JSONL_FILE_NAME = "benchmark_question_sets.jsonl"
    close = _JsonlLoader.close
    load_benchmark_question_set = _JsonlLoader._load_model
    open = _JsonlLoader.open
