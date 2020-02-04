from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node


def test_edge():
    Edge(subject="testsubject", relation="testrelation", object_="testobject", datasource="test")
