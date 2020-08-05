from collections import Counter
from enum import Enum, auto
from typing import Union
from urllib.parse import quote

from mowgli_etl.model.concept_net_predicates import RELATED_TO
from mowgli_etl.model.kg_edge import kgEdge
from mowgli_etl.model.kg_node import kgNode
from mowgli_etl.pipeline.wdc.wdc_constants import WDC_DATASOURCE_ID, WEC_NAMESPACE


