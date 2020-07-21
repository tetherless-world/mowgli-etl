import pytest

from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.model.kg_node import KgNode


@pytest.fixture
def edge() -> KgEdge:
    return KgEdge.legacy(subject="testsubject", predicate="testrelation", object="testobject", datasource="test")


@pytest.fixture
def node() -> KgNode:
    return KgNode.legacy(id="testid", label="test label", pos="n", datasource="test")
