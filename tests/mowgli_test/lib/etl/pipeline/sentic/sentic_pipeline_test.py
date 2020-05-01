from configargparse import ArgParser

from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl.pipeline.sentic.sentic_pipeline import SenticPipeline
from mowgli.lib.etl.pipeline_wrapper import PipelineWrapper


def test_sentic_pipeline(
    pipeline_storage,
    strengths,
    sample_sentic_edges,
    sample_sentic_nodes,
    url,
    senticclient,
):
    argparse = ArgParser()
    SenticPipeline.add_arguments(argparse)

    args = argparse.parse_args(["--sentic_zip_url", url, "--owl_filename", "test_data-master/test_data.owl"])
    pipeline_kwds = vars(args).copy()
    pipeline_kwds["http_client"] = senticclient
    sentic_pipeline = SenticPipeline(**pipeline_kwds)
    pipeline_wrapper = PipelineWrapper(sentic_pipeline, pipeline_storage)

    extract_kwds = pipeline_wrapper.extract()
    graph_generator = pipeline_wrapper.transform(**extract_kwds)

    nodes, edges = set(), set()
    for node_or_edge in graph_generator:
        if isinstance(node_or_edge, Node):
            nodes.add(node_or_edge)
        elif isinstance(node_or_edge, Edge):
            edges.add(node_or_edge)

    assert nodes == sample_sentic_nodes
    assert edges == sample_sentic_edges
