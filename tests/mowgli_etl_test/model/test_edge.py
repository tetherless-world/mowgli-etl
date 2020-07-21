import pytest

from mowgli_etl.model.kg_edge import KgEdge


@pytest.fixture
def edge():
    return KgEdge.legacy(subject="testsubject", predicate="testrelation", object="testobject", datasource="test",
                other={"test": 1})


def test_construction(edge: KgEdge):
    pass


def test_hash(edge: KgEdge):
    hash(edge)
