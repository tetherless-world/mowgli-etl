from pathlib import Path
from typing import Generator, Union

import pytest
from itertools import count

from mowgli_etl.cskg.edge import Edge
from mowgli_etl.cskg.node import Node
from mowgli_etl.pipeline_storage import PipelineStorage


@pytest.fixture
def cskg_edges_csv_file_path() -> Path:
    return Path(__file__).parent / "pipeline" / "cskg_csv" / "edges.csv"


@pytest.fixture
def cskg_nodes_csv_file_path() -> Path:
    return Path(__file__).parent / "pipeline" / "cskg_csv" / "nodes.csv"


@pytest.fixture
def pipeline_storage(tmp_path_factory) -> PipelineStorage:
    """
    Return a file pipeline storage wrapping a test directory that is removed after testing.
    """
    yield PipelineStorage(root_data_dir_path=tmp_path_factory.mktemp("test"), pipeline_id="test")


@pytest.fixture
def graph_generator() -> Generator[Union[Node, Edge], None, None]:
    """
    Return a generator that yields test nodes and edges
    """
    def _generator():
        nid_counter = count(1)
        while True:
            nodes = tuple(
                Node(
                    datasource='test_datasource',
                    id=f'test_node_{next(nid_counter)}',
                    label='test node'
                )
                for _ in range(2)
            )
            yield from nodes
            yield Edge(
                datasource='test_datasource',
                object=nodes[1].id,
                predicate='test_predicate',
                subject=nodes[0].id
            )
    return _generator()
