from typing import Union

from mowgli_etl.model.edge import Edge
from mowgli_etl.model.node import Node
from mowgli_etl.model.path import Path

Model = Union[Edge, Node, Path]
