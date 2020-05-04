import pytest

from mowgli.lib.cskg import mowgli_predicates
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl.mapper.concept_net.concept_net_mapper import ConceptNetMapper

try:
    from mowgli.lib.etl.mapper.concept_net.concept_net_index import ConceptNetIndex
except ImportError:
    ConceptNetIndex = None

if ConceptNetIndex is not None:
    @pytest.fixture
    def concept_net_mapper(concept_net_index: ConceptNetIndex):
        return ConceptNetMapper(concept_net_index)


    def test_map_unqualified_node(concept_net_mapper):
        edges = tuple(concept_net_mapper.map(Node(id="a", datasource="test", label="a")))
        assert len(edges) == 1
        edge = edges[0]
        assert edge.subject == "a"
        assert edge.object == "/c/en/a"
        assert edge.predicate == mowgli_predicates.SAME_AS
        assert edge.datasource == "test"


    def test_map_node_with_pos(concept_net_mapper):
        edges = tuple(concept_net_mapper.map(Node(id="nid30", datasource="test", label="30", pos="a")))
        assert len(edges) == 1
        edge = edges[0]
        assert edge.subject == "nid30"
        assert edge.object == "/c/en/30/a/wn"
        assert edge.predicate == mowgli_predicates.SAME_AS
        assert edge.datasource == "test"
