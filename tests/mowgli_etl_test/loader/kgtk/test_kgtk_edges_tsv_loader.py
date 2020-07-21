from mowgli_etl.loader.kgtk.kgtk_edges_tsv_loader import KgtkEdgesTsvLoader
from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.model.kg_node import KgNode


def test_load(graph_generator, pipeline_storage):
    with KgtkEdgesTsvLoader().open(pipeline_storage) as loader:
        loaded_edge_count = 0
        loaded_node_count = 0
        for edge_or_node in graph_generator:
            if isinstance(edge_or_node, KgNode):
                loader.load_kg_node(edge_or_node)
                loaded_node_count += 1
            elif isinstance(edge_or_node, KgEdge):
                loader.load_kg_edge(edge_or_node)
                loaded_edge_count += 1
                break
        assert loaded_edge_count == 1
        assert loaded_node_count == 2

    with open(pipeline_storage.loaded_data_dir_path / "edges.tsv") as f:
        contents = f.read()
        assert contents == """\
node1\trelation\tnode2\tnode1;label\tnode2;label\trelation;label\trelation;dimension\tweight\tsource\torigin\tsentence\tquestion\tid
test_node_1\ttest_predicate\ttest_node_2\ttest node\ttest node\t\t\t\ttest_datasource\t\t\t\ttest_node_1-test_predicate-test_node_2
"""
