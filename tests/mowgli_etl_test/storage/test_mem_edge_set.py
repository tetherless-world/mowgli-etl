from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.storage.mem_edge_set import MemEdgeSet


def test_add(edge: KgEdge):
    MemEdgeSet().add(edge)


def test_get_extant(edge: KgEdge):
    edge_set = MemEdgeSet()
    edge_set.add(edge)
    assert edge_set.get(edge.id) == edge


def test_get_nonextant(edge: KgEdge):
    assert MemEdgeSet().get(edge.id) is None
