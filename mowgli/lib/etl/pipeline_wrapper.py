import os.path
from typing import Generator, Union

from mowgli import paths
from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl._pipeline import _Pipeline
from mowgli.lib.etl.pipeline_storage import PipelineStorage


class PipelineWrapper:
    def __init__(self, args, pipeline: _Pipeline, storage: PipelineStorage):
        self.__args = args
        self.__pipeline = pipeline
        self.__storage = storage

    def extract(self, force: bool = False):
        extract_kwds = self.__pipeline.extractor.extract(force=force, storage=self.__storage)
        return extract_kwds if extract_kwds is not None else {}

    def load(self, graph_generator: Generator[Union[Node, Edge], None, None]) -> None:
        with self.__pipeline.loader.open(storage=self.__storage) as loader:
            for node_or_edge in graph_generator:
                if isinstance(node_or_edge, Node):
                    loader.load_node(node_or_edge)
                elif isinstance(node_or_edge, Edge):
                    loader.load_edge(node_or_edge)
                else:
                    raise ValueError(type(node_or_edge))

    def transform(self, force: bool = False, **extract_kwds):
        return self.__pipeline.transformer.transform(**extract_kwds)
