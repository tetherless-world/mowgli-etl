from mowgli_etl.loader._benchmark_question_loader import _BenchmarkQuestionLoader
from mowgli_etl.loader.json._jsonl_loader import _JsonlLoader


class JsonlBenchmarkQuestionLoader(_BenchmarkQuestionLoader, _JsonlLoader):
    _JSONL_FILE_NAME = "benchmark_questions.jsonl"
    close = _JsonlLoader.close
    load_benchmark_question = _JsonlLoader._load_model
    open = _JsonlLoader.open
