from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl.pipeline_wrapper import PipelineWrapper
from mowgli.lib.etl.onto.onto_pipeline import OntoPipeline
from mowgli.lib.etl.onto.onto_constants import STRENGTH_FILE_KEY
from mowgli.lib.etl.onto.onto_transformer import ONTOTransformer
from mowgli.lib.etl.onto.onto_constants import onto_archive_path
from configargparse import ArgParser
from mowgli.paths import DATA_DIR

def test_onto_pipeline(pipeline_storage,strengths, sample_onto_edges, sample_onto_nodes,url):
    argparse = ArgParser()
    OntoPipeline.add_arguments(argparse)
    
    args = argparse.parse_args(['--onto-from-url', 'https://github.com/famildtesting/test_data/archive/master.zip',
                    '--target', 'test_data.owl'])
    pipeline_kwds = vars(args).copy()
    onto_pipeline = OntoPipeline(**pipeline_kwds)
    pipeline_wrapper = PipelineWrapper(onto_pipeline, pipeline_storage)

    extract_kwds = pipeline_wrapper.extract()
    graph_generator = pipeline_wrapper.transform(**extract_kwds)


    nodes, edges = set(), set()
    for node_or_edge in graph_generator:
        if isinstance(node_or_edge, Node):
            nodes.add(node_or_edge)
        elif isinstance(node_or_edge, Edge):
            edges.add(node_or_edge)

    assert nodes == sample_onto_nodes
    assert edges == sample_onto_edges