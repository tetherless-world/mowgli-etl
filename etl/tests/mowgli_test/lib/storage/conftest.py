import pytest

from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node


@pytest.fixture
def edge() -> Edge:
    return Edge(subject="testsubject", predicate="testrelation", object="testobject", datasource="test")


@pytest.fixture
def node() -> Node:
    return Node(id="testid", label="test label", pos="n", datasource="test")
