import pytest

from mowgli import paths
from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl.cskg.cskg_csv_extractor import CskgCsvExtractor
from mowgli.lib.etl.cskg.cskg_csv_transformer import CskgCsvTransformer


@pytest.fixture
def cskg_csv_dir_path():
    return paths.DATA_DIR / "eat" / "loaded"


@pytest.fixture
def cskg_csv_extract_result(cskg_csv_dir_path):
    return CskgCsvExtractor(extracted_data_dir_path=cskg_csv_dir_path).extract()


def test_transform(cskg_csv_extract_result):
    transformer = CskgCsvTransformer()
    edges_by_subject_id = {}
    nodes_by_id = {}
    for node_or_edge in transformer.transform(**cskg_csv_extract_result):
        if isinstance(node_or_edge, Edge):
            edges_by_subject_id.setdefault(node_or_edge.subject, []).append(node_or_edge)
        elif isinstance(node_or_edge, Node):
            nodes_by_id[node_or_edge.id] = node_or_edge
    assert "eat:SPECIAL" in nodes_by_id
    assert "eat:ABILITY" in edges_by_subject_id
