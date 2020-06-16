from mowgli_etl.loader._benchmark_answer_loader import _BenchmarkAnswerLoader
from mowgli_etl.loader._benchmark_question_loader import _BenchmarkQuestionLoader
from mowgli_etl.loader._benchmark_submission_loader import _BenchmarkSubmissionLoader
from mowgli_etl.loader.json._jsonl_loader import _JsonlLoader


class JsonlBenchmarkAnswerLoader(_BenchmarkAnswerLoader, _JsonlLoader):
    _JSONL_FILE_NAME = "benchmark_answers.jsonl"
    close = _JsonlLoader.close
    load_benchmark_answer = _JsonlLoader._load_model
    open = _JsonlLoader.open
