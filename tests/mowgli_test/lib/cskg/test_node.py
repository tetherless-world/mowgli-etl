from mowgli.lib.cskg.node import Node


def test_constructor():
    Node(id="testid", label="test label", pos="n", datasource="test")
