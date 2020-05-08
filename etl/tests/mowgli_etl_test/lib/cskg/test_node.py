import pytest

from mowgli_etl.lib.cskg.node import Node


@pytest.fixture
def node():
    return Node(id="testid", label="test label", pos="n", datasource="test", other={"test": 1})


def test_constructor(node: Node):
    pass


def test_hash(node: Node):
    hash(node)
