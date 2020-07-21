from mowgli_etl.model.kg_edge import KgEdge

try:
    from mowgli_etl.storage.persistent_edge_set import PersistentEdgeSet
except ImportError:
    PersistentEdgeSet = None

if PersistentEdgeSet is not None:
    def test_construction(tmpdir):
        edge_set = PersistentEdgeSet(directory_path=tmpdir.mkdir("test"), create_if_missing=True)
        with edge_set as edge_set:
            pass
        assert edge_set.closed


    def test_add(edge: KgEdge, tmpdir):
        with PersistentEdgeSet(directory_path=tmpdir.mkdir("test"), create_if_missing=True) as edge_set:
            edge_set.add(edge)


    def test_get_extant(edge: KgEdge, tmpdir):
        with PersistentEdgeSet(directory_path=tmpdir.mkdir("test"), create_if_missing=True) as edge_set:
            edge_set.add(edge)
            assert edge_set.get(edge.id) == edge


    def test_get_nonextant(edge: KgEdge, tmpdir):
        with PersistentEdgeSet(directory_path=tmpdir.mkdir("test"), create_if_missing=True) as edge_set:
            assert edge_set.get(edge.id) is None
