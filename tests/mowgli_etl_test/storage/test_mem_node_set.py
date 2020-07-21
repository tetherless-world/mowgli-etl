from mowgli_etl.model.kg_node import KgNode
from mowgli_etl.storage.mem_node_set import MemNodeSet


def test_add(node: KgNode):
    MemNodeSet().add(node)


def test_delete(node: KgNode, tmpdir):
    node_set = MemNodeSet()
    node_set.add(node)
    assert node.id in node_set
    node_set.delete(node.id)
    assert node.id not in node_set


def test_get_extant(node: KgNode):
    node_set = MemNodeSet()
    node_set.add(node)
    assert node_set.get(node_id=node.id) == node


def test_get_nonextant(node: KgNode):
    assert MemNodeSet().get(node_id=node.id) is None
