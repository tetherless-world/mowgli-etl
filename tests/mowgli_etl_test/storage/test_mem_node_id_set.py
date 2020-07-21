from mowgli_etl.model.kg_node import KgNode
from mowgli_etl.storage.mem_node_id_set import MemNodeIdSet


def test_add(node: KgNode):
    MemNodeIdSet().add(node.id)


def test_get_extant(node: KgNode):
    node_id_set = MemNodeIdSet()
    node_id_set.add(node.id)
    assert node.id in node_id_set


def test_get_nonextant(node: KgNode):
    assert node.id not in MemNodeIdSet()
