from pathlib import Path

from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.pipeline.wdc.wdc_constants import WDC_DATASOURCE_ID
from mowgli_etl.pipeline.wdc.wdc_transformer import WDCTransformer


def test_transform(wdc_jsonl_file_path: Path):
    edges = []
    for edge in WDCTransformer().transform(wdc_jsonl_file_path=wdc_jsonl_file_path):
        assert isinstance(edge, KgEdge)
        assert edge.id
        # assert edge.sources == (WDC_DATASOURCE_ID,)
        edges.append(edge)
        if len(edges) == 100:
            break
    assert len(edges) == 100
