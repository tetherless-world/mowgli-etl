import pytest

from mowgli_etl.cskg.edge import Edge
from mowgli_etl.cskg.node import Node


@pytest.fixture
def edge() -> Edge:
    return Edge(subject="testsubject", predicate="testrelation", object="testobject", datasource="test")


@pytest.fixture
def node() -> Node:
    return Node(id="testid", label="test label", pos="n", datasource="test")
