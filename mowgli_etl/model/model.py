from typing import Union

from mowgli_etl.model.benchmark import Benchmark
from mowgli_etl.model.benchmark_question import BenchmarkQuestion
from mowgli_etl.model.benchmark_dataset import BenchmarkDataset
from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.model.kg_node import KgNode
from mowgli_etl.model.kg_path import KgPath

Model = Union[Benchmark, BenchmarkQuestion, BenchmarkDataset, KgEdge, KgNode, KgPath]
