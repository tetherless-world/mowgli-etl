from mowgli.lib.cskg.node import Node
from mowgli.lib.storage.mem_node_id_set import MemNodeIdSet


def test_add(node: Node):
    MemNodeIdSet().add(node.id)


def test_get_extant(node: Node):
    node_id_set = MemNodeIdSet()
    node_id_set.add(node.id)
    assert node.id in node_id_set


def test_get_nonextant(node: Node):
    assert node.id not in MemNodeIdSet()
