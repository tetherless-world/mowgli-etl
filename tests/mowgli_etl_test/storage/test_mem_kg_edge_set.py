from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.storage.mem_kg_edge_set import MemKgEdgeSet


def test_add(edge: KgEdge):
    MemKgEdgeSet().add(edge)


def test_get_extant(edge: KgEdge):
    edge_set = MemKgEdgeSet()
    edge_set.add(edge)
    assert edge_set.get(edge.id) == edge


def test_get_nonextant(edge: KgEdge):
    assert MemKgEdgeSet().get(edge.id) is None
