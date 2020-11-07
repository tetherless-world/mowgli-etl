from pathlib import Path

from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.pipeline.wdc.wdc_constants import WDC_DATASOURCE_ID
from mowgli_etl.pipeline.wdc.wdc_transformer import WdcTransformer
from mowgli_etl.pipeline.wdc.wdc_heuristic_product_type_classifier import WdcHeuristicProductTypeClassifier
from mowgli_etl.pipeline.wdc.parsimonious_parser.wdc_parsimonious_dimension_parser import WdcParsimoniousDimensionParser

def test_transform(wdc_jsonl_file_path: Path):
    edges = []
    for edge in WdcTransformer().transform(wdc_jsonl_file_path=wdc_jsonl_file_path, wdc_product_type_classifier=WdcHeuristicProductTypeClassifier(), wdc_dimension_parser=None):
        assert isinstance(edge, KgEdge)
        assert edge.id
        assert edge.source_ids == (WDC_DATASOURCE_ID,)
        edges.append(edge)
        if len(edges) == 100:
            break
    assert len(edges) == 100
