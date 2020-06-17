from typing import Union

from mowgli_etl.model.benchmark import Benchmark
from mowgli_etl.model.benchmark_question import BenchmarkQuestion
from mowgli_etl.model.benchmark_dataset import BenchmarkDataset
from mowgli_etl.model.edge import Edge
from mowgli_etl.model.node import Node
from mowgli_etl.model.path import Path

Model = Union[Benchmark, BenchmarkQuestion, BenchmarkDataset, Edge, Node, Path]
