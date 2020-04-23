import logging
from typing import Generator, Union, Dict

from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl._pipeline import _Pipeline
from mowgli.lib.etl.pipeline_storage import PipelineStorage


class PipelineWrapper:
    def __init__(self, pipeline: _Pipeline, storage: PipelineStorage):
        self._logger = logging.getLogger(self.__class__.__name__)
        self.__pipeline = pipeline
        self.__storage = storage

    def extract(self, force: bool = False) -> Dict[str, object]:
        extract_kwds = self.__pipeline.extractor.extract(force=force, storage=self.__storage)
        return extract_kwds if extract_kwds is not None else {}

    def extract_transform_load(self, force: bool = False, dupe_check: bool = True):
        extract_kwds = self.extract(force=force)
        graph_generator = self.transform(force=force, dupe_check=dupe_check, **extract_kwds)
        self.load(graph_generator)

    @property
    def id(self) -> str:
        return self.__pipeline.id

    def load(self, graph_generator: Generator[Union[Node, Edge], None, None]) -> None:
        with self.__pipeline.loader.open(storage=self.__storage) as loader:
            for node_or_edge in graph_generator:
                if isinstance(node_or_edge, Node):
                    loader.load_node(node_or_edge)
                elif isinstance(node_or_edge, Edge):
                    loader.load_edge(node_or_edge)
                else:
                    raise ValueError(type(node_or_edge))

    def transform(self, force: bool = False, dupe_check: bool = True, **extract_kwds) -> Generator[Union[Edge, Node], None, None]:
        edges_by_signature = {}
        nodes_by_id = {}
        node_ids_used_by_edges = set()

        if not dupe_check:
            self._logger.info("Skipping duplicate checking during transform")

        for node_or_edge in self.__pipeline.transformer.transform(**extract_kwds):
            if dupe_check:
                if isinstance(node_or_edge, Node):
                    node = node_or_edge
                    # Node ID's should be unique in the CSKG.
                    existing_node = nodes_by_id.get(node.id)
                    if existing_node is not None:
                        if existing_node == node:
                            # Common case: ignore exact duplicate nodes i.e., nodes that are the same in all fields.
                            # This happens frequently in the word association sources, where the same word can come
                            # up as a response to multiple cues.
                            continue
                        else:
                            # Throw an exception if two nodes have the same id but aren't the same in all of their fields
                            raise ValueError(
                                "nodes with same id, different contents: original=%s, duplicate=%s" % (existing_node, node))
                    else:
                        nodes_by_id[node.id] = node
                elif isinstance(node_or_edge, Edge):
                    edge = node_or_edge
                    # Edges should be unique in the CSKG, meaning that the tuple of (subject, predicate, object) should be unique.
                    existing_subject_edges = edges_by_signature.setdefault(edge.subject, {})
                    existing_predicate_edges = existing_subject_edges.setdefault(edge.predicate, {})
                    existing_object_edge = existing_predicate_edges.get(edge.object)
                    if existing_object_edge is not None:
                        # Don't try to handle the exact duplicate case differently. It should never happen.
                        raise ValueError("duplicate edge: original=%s, duplicate=%s" % (existing_object_edge, edge))
                    existing_predicate_edges[edge.object] = edge
                    node_ids_used_by_edges.add(edge.subject)
                    node_ids_used_by_edges.add(edge.object)
            yield node_or_edge
        for node_id in nodes_by_id.keys():
            if node_id not in node_ids_used_by_edges:
                raise ValueError("node %s not used by an edges: " % node_id)
