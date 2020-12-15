from pathlib import Path

from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.pipeline.wdc.wdc_constants import WDC_DATASOURCE_ID
from mowgli_etl.pipeline.wdc.wdc_transformer import WdcTransformer
from mowgli_etl.pipeline.wdc.wdc_heuristic_product_type_classifier import (
    WdcHeuristicProductTypeClassifier,
)
from mowgli_etl.pipeline.wdc.parsimonious_parser.wdc_parsimonious_dimension_parser import (
    WdcParsimoniousDimensionParser,
)
from mowgli_etl.pipeline.wdc.wdc_offers_corpus import WdcOffersCorpus

# Need to write actual tests
def test_wdc_transform(wdc_large_offers_corpus: WdcOffersCorpus):
    transformer = WdcTransformer()
    edges = []
    node_ids = set()
    predicates = set()
    for result in transformer.transform(corpus=wdc_large_offers_corpus):
        assert isinstance(result, KgEdge)
        edges.append(result)
        node_ids.add(result.object)
        node_ids.add(result.subject)
        predicates.add(result.predicate)

    for edge in edges:
        assert edge.subject in node_ids
        assert edge.object in node_ids
        assert edge.predicate in predicates
