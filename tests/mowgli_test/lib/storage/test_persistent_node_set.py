from mowgli.lib.cskg.node import Node

try:
    from mowgli.lib.storage.persistent_node_set import PersistentNodeSet
except ImportError:
    PersistentNodeSet = None


if PersistentNodeSet is not None:
    def test_construction(tmpdir):
        node_set = PersistentNodeSet(directory_path=tmpdir.mkdir("test"), create_if_missing=True)
        with node_set as node_set:
            pass
        assert node_set.closed


    def test_add(node: Node, tmpdir):
        with PersistentNodeSet(directory_path=tmpdir.mkdir("test"), create_if_missing=True) as node_set:
            node_set.add(node)


    def test_get_extant(node: Node, tmpdir):
        with PersistentNodeSet(directory_path=tmpdir.mkdir("test"), create_if_missing=True) as node_set:
            node_set.add(node)
            assert node_set.get(node_id=node.id) == node


    def test_get_nonextant(node: Node, tmpdir):
        with PersistentNodeSet(directory_path=tmpdir.mkdir("test"), create_if_missing=True) as node_set:
            assert node_set.get(node_id=node.id) is None
