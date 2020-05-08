from mowgli_etl.lib.cskg.node import Node
from mowgli_etl.lib.storage.mem_node_set import MemNodeSet


def test_add(node: Node):
    MemNodeSet().add(node)


def test_delete(node: Node, tmpdir):
    node_set = MemNodeSet()
    node_set.add(node)
    assert node.id in node_set
    node_set.delete(node.id)
    assert node.id not in node_set


def test_get_extant(node: Node):
    node_set = MemNodeSet()
    node_set.add(node)
    assert node_set.get(node_id=node.id) == node


def test_get_nonextant(node: Node):
    assert MemNodeSet().get(node_id=node.id) is None
