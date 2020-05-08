import pytest

from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl.pipeline.cskg_csv.cskg_csv_extractor import CskgCsvExtractor
from mowgli.lib.etl.pipeline.cskg_csv.cskg_csv_transformer import CskgCsvTransformer


@pytest.fixture
def cskg_csv_extract_result(cskg_edges_csv_file_path, cskg_nodes_csv_file_path):
    return CskgCsvExtractor(edges_csv_file_paths=(cskg_edges_csv_file_path,),
                            nodes_csv_file_paths=(cskg_nodes_csv_file_path,)).extract()


def test_transform(cskg_csv_extract_result):
    transformer = CskgCsvTransformer()
    edges_by_subject_id = {}
    nodes_by_id = {}
    for node_or_edge in transformer.transform(**cskg_csv_extract_result):
        if isinstance(node_or_edge, Edge):
            edges_by_subject_id.setdefault(node_or_edge.subject, []).append(node_or_edge)
        elif isinstance(node_or_edge, Node):
            nodes_by_id[node_or_edge.id] = node_or_edge
    assert "swow:a" in nodes_by_id
    assert "swow:a" in edges_by_subject_id
