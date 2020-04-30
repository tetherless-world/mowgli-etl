from mowgli.lib.cskg.edge import Edge

try:
    from mowgli.lib.storage.edge_set import PersistentEdgeSet
except ImportError:
    PersistentEdgeSet = None


def test_construction(tmpdir):
    if PersistentEdgeSet is None:
        return

    edge_set = PersistentEdgeSet(name=tmpdir.mkdir("test"), create_if_missing=True)
    with edge_set as edge_set:
        pass
    assert edge_set.closed


def test_add(edge: Edge, tmpdir):
    if PersistentEdgeSet is None:
        return

    with PersistentEdgeSet(name=tmpdir.mkdir("test"), create_if_missing=True) as edge_set:
        edge_set.add(edge)


def test_get_extant(edge: Edge, tmpdir):
    if PersistentEdgeSet is None:
        return

    with PersistentEdgeSet(name=tmpdir.mkdir("test"), create_if_missing=True) as edge_set:
        edge_set.add(edge)
        assert edge_set.get(object_=edge.object, predicate=edge.predicate, subject=edge.subject) == edge


def test_get_nonextant(edge: Edge, tmpdir):
    if PersistentEdgeSet is None:
        return

    with PersistentEdgeSet(name=tmpdir.mkdir("test"), create_if_missing=True) as edge_set:
        assert edge_set.get(object_=edge.object, predicate=edge.predicate, subject=edge.subject) is None
