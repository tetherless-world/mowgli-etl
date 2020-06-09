from mowgli_etl.model.edge import Edge

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


    def test_add(edge: Edge, tmpdir):
        with PersistentEdgeSet(directory_path=tmpdir.mkdir("test"), create_if_missing=True) as edge_set:
            edge_set.add(edge)


    def test_get_extant(edge: Edge, tmpdir):
        with PersistentEdgeSet(directory_path=tmpdir.mkdir("test"), create_if_missing=True) as edge_set:
            edge_set.add(edge)
            assert edge_set.get(object=edge.object, predicate=edge.predicate, subject=edge.subject) == edge


    def test_get_nonextant(edge: Edge, tmpdir):
        with PersistentEdgeSet(directory_path=tmpdir.mkdir("test"), create_if_missing=True) as edge_set:
            assert edge_set.get(object=edge.object, predicate=edge.predicate, subject=edge.subject) is None
