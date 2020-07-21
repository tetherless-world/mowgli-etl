from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.model.kg_node import KgNode
from mowgli_etl.pipeline.swow.swow_pipeline import SwowPipeline
from mowgli_etl.pipeline_wrapper import PipelineWrapper


def test_swow_pipeline(pipeline_storage, sample_archive_path, sample_swow_edges, sample_swow_nodes):
    args = {'swow_archive_path': sample_archive_path}
    swow_pipeline = SwowPipeline(**args)
    pipeline_wrapper = PipelineWrapper(swow_pipeline, pipeline_storage)

    extract_kwds = pipeline_wrapper.extract()
    graph_generator = pipeline_wrapper.transform(**extract_kwds)

    nodes, edges = set(), set()
    for node_or_edge in graph_generator:
        if isinstance(node_or_edge, KgNode):
            nodes.add(node_or_edge)
        elif isinstance(node_or_edge, KgEdge):
            edges.add(node_or_edge)

    assert nodes == sample_swow_nodes
    assert edges == sample_swow_edges
