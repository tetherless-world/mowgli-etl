import pytest

from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.model.kg_node import KgNode
from mowgli_etl.pipeline.cskg_csv.cskg_csv_extractor import CskgCsvExtractor
from mowgli_etl.pipeline.cskg_csv.cskg_csv_transformer import CskgCsvTransformer


@pytest.fixture
def cskg_csv_extract_result(cskg_edges_csv_file_path, cskg_nodes_csv_file_path):
    return CskgCsvExtractor(edges_csv_file_paths=(cskg_edges_csv_file_path,),
                            nodes_csv_file_paths=(cskg_nodes_csv_file_path,)).extract()


def test_transform(cskg_csv_extract_result):
    transformer = CskgCsvTransformer()
    edges_by_subject_id = {}
    nodes_by_id = {}
    for node_or_edge in transformer.transform(**cskg_csv_extract_result):
        if isinstance(node_or_edge, KgEdge):
            edges_by_subject_id.setdefault(node_or_edge.subject, []).append(node_or_edge)
        elif isinstance(node_or_edge, KgNode):
            nodes_by_id[node_or_edge.id] = node_or_edge
    assert "swow:a" in nodes_by_id
    assert "swow:a" in edges_by_subject_id
