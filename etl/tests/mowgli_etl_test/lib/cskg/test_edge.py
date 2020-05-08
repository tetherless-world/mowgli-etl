import pytest

from mowgli_etl.lib.cskg.edge import Edge


@pytest.fixture
def edge():
    return Edge(subject="testsubject", predicate="testrelation", object="testobject", datasource="test",
                other={"test": 1})


def test_construction(edge: Edge):
    pass


def test_hash(edge: Edge):
    hash(edge)
