import logging
import subprocess
import sys
from abc import ABC, abstractmethod
from pathlib import Path

from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.model.kg_node import KgNode
from mowgli_etl.pipeline_storage import PipelineStorage


class _Loader(ABC):
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    def _bzip_file(self, file_path: Path):
        if sys.platform.startswith("win"):
            return
        subprocess.call(["bzip2", "-9", "-f", str(file_path)])

    @abstractmethod
    def close(self) -> None:
        """
        Close this loader.
        """

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwds):
        self.close()

    @abstractmethod
    def open(self, storage: PipelineStorage):
        """
        Open this loader before calling load_* methods.
        """
        return self
