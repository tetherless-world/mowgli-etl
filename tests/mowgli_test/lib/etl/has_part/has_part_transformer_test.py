from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl.has_part.has_part_extractor import HasPartExtractor
from mowgli.lib.etl.has_part.has_part_transformer import HasPartTransformer


def test_has_part_transformer():
    extract_result = HasPartExtractor().extract()
    transformer = HasPartTransformer()

    nodes, edges = set(), set()
    for result in transformer.transform(**extract_result):
        if isinstance(result, Node):
            nodes.add(result)
        elif isinstance(result, Edge):
            edges.add(result)
