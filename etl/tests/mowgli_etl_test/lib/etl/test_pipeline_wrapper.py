from typing import Tuple, Union

from pytest import fail

from mowgli_etl.cskg.edge import Edge
from mowgli_etl.cskg.node import Node
from mowgli_etl.lib.etl._extractor import _Extractor
from mowgli_etl.lib.etl._pipeline import _Pipeline
from mowgli_etl.lib.etl._transformer import _Transformer
from mowgli_etl.pipeline_storage import PipelineStorage
from mowgli_etl.pipeline_wrapper import PipelineWrapper


class NopExtractor(_Extractor):
    def extract(self, *args, **kwds):
        return {}


class MockTransformer(_Transformer):
    def __init__(self, node_edge_sequence: Tuple[Union[Node, Edge], ...]):
        self.__node_edge_sequence = node_edge_sequence

    def transform(self, **kwds):
        yield from self.__node_edge_sequence


class MockPipeline(_Pipeline):
    def __init__(self, node_edge_sequence: Tuple[Union[Node, Edge], ...]):
        _Pipeline.__init__(
            self,
            extractor=NopExtractor(),
            id="mock",
            transformer=MockTransformer(node_edge_sequence)
        )


def run(node_edge_sequence: Tuple[Union[Node, Edge], ...], pipeline_storage: PipelineStorage):
    return PipelineWrapper(MockPipeline(node_edge_sequence), pipeline_storage).run()


SUBJECT_NODE = Node(id="testid", label="test label", pos="n", datasource="test")
EXACT_DUPLICATE_SUBJECT_NODE = Node(id="testid", label="test label", pos="n", datasource="test")
INEXACT_DUPLICATE_SUBJECT_NODE = Node(id="testid", label="test label variation", pos="n", datasource="test")
OBJECT_NODE = Node(id="testobject", label="test object", pos="n", datasource="test")
EDGE = Edge(subject=SUBJECT_NODE.id, object=OBJECT_NODE.id, predicate="test", datasource="test")


def test_exact_duplicate_node(pipeline_storage):
    # Exact duplicates are ignored
    run((SUBJECT_NODE, OBJECT_NODE, EDGE, EXACT_DUPLICATE_SUBJECT_NODE), pipeline_storage)


def test_inexact_duplicate_node(pipeline_storage):
    try:
        run((SUBJECT_NODE, OBJECT_NODE, EDGE, INEXACT_DUPLICATE_SUBJECT_NODE), pipeline_storage)
        fail()
    except ValueError:
        pass


def test_extraneous_node(pipeline_storage):
    try:
        run((SUBJECT_NODE, OBJECT_NODE,
             Edge(subject=SUBJECT_NODE.id, object="externalnode", predicate="test",
                  datasource="test")), pipeline_storage)
        fail()
    except ValueError:
        pass
