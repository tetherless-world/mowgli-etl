import pytest

from mowgli_etl.model.kg_node import KgNode


@pytest.fixture
def node():
    return KgNode(id="testid", label="test label", pos="n", datasource="test", other={"test": 1})


def test_constructor(node: KgNode):
    pass


def test_hash(node: KgNode):
    hash(node)
