from mowgli_etl.lib.cskg.edge import Edge
from mowgli_etl.lib.etl.pipeline.aristo.aristo_extractor import AristoExtractor
from mowgli_etl.lib.etl.pipeline.aristo.aristo_transformer import AristoTransformer


def test_aristo_transformer(pipeline_storage):
    extract_result = AristoExtractor().extract(force=False, storage=pipeline_storage)
    transformer = AristoTransformer()

    edges_tree = {}
    nodes_by_id = {}
    edges_by_node_id = {}
    edges = []
    for result in transformer.transform(**extract_result):
        # print(result)
        if isinstance(result, Edge):
            edge = result
            edges_by_predicate = edges_tree.setdefault(edge.subject, {}).setdefault(edge.object, {})
            assert edge.predicate not in edges_by_predicate
            edges_by_predicate[edge.predicate] = edge
            for node_id in (edge.subject, edge.object):
                edges_by_node_id.setdefault(node_id, []).append(edge)
            edges.append(edge)
        else:
            node = result
            assert node.id not in nodes_by_id
            nodes_by_id[node.id] = node
    for edge in edges:
        assert edge.subject in nodes_by_id
        assert edge.object in nodes_by_id or edge.object.startswith("wn:")
    for node in nodes_by_id.values():
        edges_by_node_id[node.id]
