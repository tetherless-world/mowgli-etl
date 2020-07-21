from mowgli_etl.loader.kgtk.kgtk_edges_tsv_loader import KgtkEdgesTsvLoader
from mowgli_etl.model.edge import Edge
from mowgli_etl.model.node import Node


def test_load(graph_generator, pipeline_storage):
    with KgtkEdgesTsvLoader().open(pipeline_storage) as loader:
        loaded_edge_count = 0
        loaded_node_count = 0
        for edge_or_node in graph_generator:
            if isinstance(edge_or_node, Node):
                loader.load_node(edge_or_node)
                loaded_node_count += 1
            elif isinstance(edge_or_node, Edge):
                loader.load_edge(edge_or_node)
                loaded_edge_count += 1
        assert loaded_edge_count == 1
        assert loaded_node_count == 2

    with open(pipeline_storage.loaded_data_dir_path / "edges.tsv") as f:
        assert f.read() == """\
"""
