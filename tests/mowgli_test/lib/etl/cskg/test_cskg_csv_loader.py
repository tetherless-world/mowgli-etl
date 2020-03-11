from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl.cskg.cskg_csv_loader import CskgCsvLoader

_EXPECTED_NODE_HEADER = 'id\tlabel\taliases\tpos\tdatasource\tother'
_EXPECTED_EDGE_HEADER = 'subject\tpredicate\tobject\tdatasource\tweight\tother'


def test_write_node(pipeline_storage):
    test_node = Node(
        datasource='test_datasource',
        id='test_nid',
        label='Test Node',
        aliases=('t-node', 'Node Test'),
        other={'datasets': ['test_dataset', 'other_test_dataset']},
        pos='N'
    )

    with CskgCsvLoader().open(pipeline_storage) as loader:
        loader.load_node(test_node)
        # 20200310 MG: duplicate removal has been moved to the PipelineWrapper
        # loader.load_node(test_node)

    expected_node_text = (
            _EXPECTED_NODE_HEADER + '\n'
            + 'test_nid\tTest Node\tt-node Node Test\tN\ttest_datasource\t'
            + "{'datasets': ['test_dataset', 'other_test_dataset']}\n"
    )

    with open(pipeline_storage.loaded_data_dir_path / "edges.csv") as f:
        assert f.read() == _EXPECTED_EDGE_HEADER + '\n'

    with open(pipeline_storage.loaded_data_dir_path / "nodes.csv") as f:
        assert f.read() == expected_node_text


def test_write_edge(pipeline_storage):
    test_edge = Edge(
        datasource='test_datasource',
        object_='test_obj',
        predicate='test_rel',
        subject='test_subject',
        other={'datasets': ['test_dataset', 'other_test_dataset']},
        weight=0.999
    )

    with CskgCsvLoader().open(pipeline_storage) as loader:
        loader.load_edge(test_edge)
        # Load twice to test handling of redundant edges
        # 20200310 MG: duplicate removal has been moved to the PipelineWrapper
        # loader.load_edge(test_edge)

    expected_edge_text = (
            _EXPECTED_EDGE_HEADER + '\n'
            + 'test_subject\ttest_rel\ttest_obj\ttest_datasource\t0.999\t'
            + "{'datasets': ['test_dataset', 'other_test_dataset']}\n"
    )

    with open(pipeline_storage.loaded_data_dir_path / "edges.csv") as f:
        assert f.read() == expected_edge_text

    with open(pipeline_storage.loaded_data_dir_path / "nodes.csv") as f:
        assert f.read() == _EXPECTED_NODE_HEADER + '\n'
