from mowgli_etl.loader._path_loader import _PathLoader
from mowgli_etl.loader.json._jsonl_loader import _JsonlLoader


class JsonlPathLoader(_PathLoader, _JsonlLoader):
    _JSONL_FILE_NAME = "paths.jsonl"
    close = _JsonlLoader.close
    load_path = _JsonlLoader._load_model
    open = _JsonlLoader.open
