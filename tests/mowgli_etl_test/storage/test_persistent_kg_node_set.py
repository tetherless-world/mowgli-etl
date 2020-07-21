from mowgli_etl.model.kg_node import KgNode

try:
    from mowgli_etl.storage.persistent_kg_node_set import PersistentKgNodeSet
except ImportError:
    PersistentKgNodeSet = None


if PersistentKgNodeSet is not None:
    def test_construction(tmpdir):
        node_set = PersistentKgNodeSet(directory_path=tmpdir.mkdir("test"), create_if_missing=True)
        with node_set as node_set:
            pass
        assert node_set.closed


    def test_add(node: KgNode, tmpdir):
        with PersistentKgNodeSet(directory_path=tmpdir.mkdir("test"), create_if_missing=True) as node_set:
            node_set.add(node)


    def test_delete(node: KgNode, tmpdir):
        with PersistentKgNodeSet(directory_path=tmpdir.mkdir("test"), create_if_missing=True) as node_set:
            node_set.add(node)
            assert node.id in node_set
            node_set.delete(node.id)
            assert node.id not in node_set


    def test_get_extant(node: KgNode, tmpdir):
        with PersistentKgNodeSet(directory_path=tmpdir.mkdir("test"), create_if_missing=True) as node_set:
            node_set.add(node)
            assert node_set.get(node_id=node.id) == node


    def test_get_nonextant(node: KgNode, tmpdir):
        with PersistentKgNodeSet(directory_path=tmpdir.mkdir("test"), create_if_missing=True) as node_set:
            assert node_set.get(node_id=node.id) is None
