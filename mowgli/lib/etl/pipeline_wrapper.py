import logging
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Generator, Union, Dict, Optional

from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl._pipeline import _Pipeline
from mowgli.lib.etl.pipeline_storage import PipelineStorage
from mowgli.lib.storage._edge_set import _EdgeSet
from mowgli.lib.storage._node_id_set import _NodeIdSet
from mowgli.lib.storage._node_set import _NodeSet
from mowgli.lib.storage.mem_edge_set import MemEdgeSet
from mowgli.lib.storage.mem_node_id_set import MemNodeIdSet
from mowgli.lib.storage.mem_node_set import MemNodeSet

try:
    from mowgli.lib.storage.persistent_edge_set import PersistentEdgeSet
    from mowgli.lib.storage.persistent_node_id_set import PersistentNodeIdSet
    from mowgli.lib.storage.persistent_node_set import PersistentNodeSet
except ImportError:
    PersistentEdgeSet = PersistentNodeSet = PersistentNodeIdSet = None


class PipelineWrapper:
    def __init__(self, pipeline: _Pipeline, storage: PipelineStorage):
        self._logger = logging.getLogger(self.__class__.__name__)
        self.__pipeline = pipeline
        self.__storage = storage

    def extract(self, force: bool = False) -> Dict[str, object]:
        extract_kwds = self.__pipeline.extractor.extract(
            force=force, storage=self.__storage
        )
        return extract_kwds if extract_kwds is not None else {}

    def extract_transform_load(
        self, force: bool = False, skip_whole_graph_check: Optional[bool] = False
    ):
        extract_kwds = self.extract(force=force)
        graph_generator = self.transform(
            force=force, skip_whole_graph_check=skip_whole_graph_check, **extract_kwds
        )
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

    def transform(
            self,
            force: bool = False,
            skip_whole_graph_check: Optional[bool] = False,
            **extract_kwds
    ) -> Generator[Union[Edge, Node], None, None]:
        transform_generator = self.__pipeline.transformer.transform(**extract_kwds)

        if skip_whole_graph_check:
            self._logger.info("skipping whole graph checking during transform")
            yield from transform_generator
            return

        if PersistentEdgeSet is not None:
            with TemporaryDirectory() as temp_dir:
                temp_dir_path = Path(temp_dir)
                with PersistentEdgeSet(name=temp_dir_path / "edges", create_if_missing=True) as edge_set:
                    with PersistentNodeSet(name=temp_dir_path / "nodes", create_if_missing=True) as node_set:
                        with PersistentNodeIdSet(name=temp_dir_path / "used_node_ids",
                                                 create_if_missing=True) as used_node_ids_set:
                            yield from self.__transform(
                                edge_set=edge_set,
                                node_set=node_set,
                                transform_generator=transform_generator,
                                used_node_ids_set=used_node_ids_set
                            )
        else:
            yield from self.__transform(
                edge_set=MemEdgeSet(),
                node_set=MemNodeSet(),
                transform_generator=transform_generator,
                used_node_ids_set=MemNodeIdSet()
            )

    def __transform(
            self,
            *,
            edge_set: _EdgeSet,
            node_set: _NodeSet,
            transform_generator: Generator[Union[Edge, Node], None, None],
            used_node_ids_set: _NodeIdSet
    ) -> Generator[Union[Edge, Node], None, None]:
        for node_or_edge in transform_generator:
            if isinstance(node_or_edge, Node):
                node = node_or_edge
                # Node ID's should be unique in the CSKG.
                existing_node = node_set.get(node.id)
                if existing_node is not None:
                    if existing_node == node:
                        # Common case: ignore exact duplicate nodes i.e., nodes that are the same in all fields.
                        # This happens frequently in the word association sources, where the same word can come
                        # up as a response to multiple cues.
                        continue
                    else:
                        # Throw an exception if two nodes have the same id but aren't the same in all of their fields
                        raise ValueError(
                            "nodes with same id, different contents: original=%s, duplicate=%s"
                            % (existing_node, node)
                        )
                else:
                    node_set.add(node)
            elif isinstance(node_or_edge, Edge):
                edge = node_or_edge
                # Edges should be unique in the CSKG, meaning that the tuple of (subject, predicate, object) should be unique.
                existing_edge = edge_set.get(object_=edge.object, predicate=edge.predicate,
                                             subject=edge.subject)
                if existing_edge is not None:
                    # Don't try to handle the exact duplicate case differently. It should never happen.
                    raise ValueError(
                        "duplicate edge: original=%s, duplicate=%s"
                        % (existing_edge, edge)
                    )
                edge_set.add(edge)
                used_node_ids_set.add(edge.subject)
                used_node_ids_set.add(edge.object)
            yield node_or_edge
        for node_id in node_set.keys():
            if node_id not in used_node_ids_set:
                raise ValueError("node %s not used by an edge" % node_id)
