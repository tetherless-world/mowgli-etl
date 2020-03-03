from mowgli.lib.cskg.edge import Edge


def test_edge():
    Edge(subject="testsubject", predicate="testrelation", object_="testobject", datasource="test")
