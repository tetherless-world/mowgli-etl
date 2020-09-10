import pytest

from mowgli_etl.model import mowgli_predicates
from mowgli_etl.model.kg_node import KgNode

try:
    from mowgli_etl.mapper.concept_net.concept_net_mapper import ConceptNetMapper
except ImportError:
    ConceptNetMapper = None

if ConceptNetMapper is not None:
    @pytest.fixture
    def concept_net_mapper(concept_net_index):
        return ConceptNetMapper(concept_net_index)


    def test_map_unqualified_node(concept_net_mapper):
        edges = tuple(concept_net_mapper.map(KgNode.legacy(id="a", datasource="test", label="a")))
        assert len(edges) == 1
        edge = edges[0]
        assert edge.subject == "a"
        assert edge.object == "/c/en/a"
        assert edge.predicate == mowgli_predicates.SAME_AS
        assert edge.source_ids == ("test",)


    def test_map_node_with_pos(concept_net_mapper):
        edges = tuple(concept_net_mapper.map(KgNode.legacy(id="nid30", datasource="test", label="30", pos="a")))
        assert len(edges) == 1
        edge = edges[0]
        assert edge.subject == "nid30"
        assert edge.object == "/c/en/30/a/wn"
        assert edge.predicate == mowgli_predicates.SAME_AS
        assert edge.source_ids == ("test",)
