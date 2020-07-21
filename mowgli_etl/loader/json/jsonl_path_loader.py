from mowgli_etl.loader._kg_path_loader import _KgPathLoader
from mowgli_etl.loader.json._jsonl_loader import _JsonlLoader


class JsonlPathLoader(_KgPathLoader, _JsonlLoader):
    _JSONL_FILE_NAME = "paths.jsonl"
    close = _JsonlLoader.close
    load_kg_path = _JsonlLoader._load_model
    open = _JsonlLoader.open
