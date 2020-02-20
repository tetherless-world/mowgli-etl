import io

from mowgli.lib.cskg.node import Node
from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.loader.csv_cskg_loader import CsvCskgLoader

_EXPECTED_NODE_HEADER = 'id\tlabel\taliases\tpos\tdatasource\tother'
_EXPECTED_EDGE_HEADER = 'subject\tpredicate\tobject\tdatasource\tweight\tother'

def test_write_node():
    node_buffer = io.StringIO()
    edge_buffer = io.StringIO()

    test_node = Node(
        datasource='test_datasource',
        id='test_nid',
        label='Test Node',
        aliases=('t-node', 'Node Test'),
        other={'datasets': ['test_dataset', 'other_test_dataset']},
        pos='N'
    )

    loader = CsvCskgLoader(node_file=node_buffer, edge_file=edge_buffer)

    loader.load_node(test_node)

    expected_node_text = (
        _EXPECTED_NODE_HEADER + '\n'
        + 'test_nid\tTest Node\tt-node Node Test\tN\ttest_datasource\t'
        + "{'datasets': ['test_dataset', 'other_test_dataset']}\n"
    )

    assert node_buffer.getvalue() == expected_node_text

    assert edge_buffer.getvalue() == _EXPECTED_EDGE_HEADER + '\n'

def test_write_edge():
    node_buffer = io.StringIO()
    edge_buffer = io.StringIO()

    test_edge = Edge(
        datasource='test_datasource',
        object_='test_obj',
        relation='test_rel',
        subject='test_subject',
        other={'datasets': ['test_dataset', 'other_test_dataset']},
        weight=0.999
    )

    loader = CsvCskgLoader(node_file=node_buffer, edge_file=edge_buffer)

    loader.load_edge(test_edge)

    expected_edge_text = (
        _EXPECTED_EDGE_HEADER + '\n'
        + 'test_subject\ttest_rel\ttest_obj\ttest_datasource\t0.999\t'
        + "{'datasets': ['test_dataset', 'other_test_dataset']}\n"
    )

    assert edge_buffer.getvalue() == expected_edge_text

    assert node_buffer.getvalue() == _EXPECTED_NODE_HEADER + '\n'