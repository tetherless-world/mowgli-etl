from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl.usf.usf_transformer import USFTransformer
from mowgli.lib.etl.usf.usf_mappers import usf_edge, usf_node
import pathlib
import os

def test_transform():
    