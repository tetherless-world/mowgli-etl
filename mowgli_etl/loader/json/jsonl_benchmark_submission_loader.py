from mowgli_etl.loader._benchmark_question_loader import _BenchmarkQuestionLoader
from mowgli_etl.loader._benchmark_submission_loader import _BenchmarkSubmissionLoader
from mowgli_etl.loader.json._jsonl_loader import _JsonlLoader


class JsonlBenchmarkSubmissionLoader(_BenchmarkSubmissionLoader, _JsonlLoader):
    _JSONL_FILE_NAME = "benchmark_submissions.jsonl"
    close = _JsonlLoader.close
    load_benchmark_submission = _JsonlLoader._load_model
    open = _JsonlLoader.open
