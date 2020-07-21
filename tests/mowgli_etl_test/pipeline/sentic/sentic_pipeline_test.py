from configargparse import ArgParser

from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.model.kg_node import KgNode
from mowgli_etl.pipeline.sentic import sentic_types
from mowgli_etl.pipeline.sentic.sentic_constants import SENTIC_TYPE_KEY
from mowgli_etl.pipeline.sentic.sentic_pipeline import SenticPipeline
from mowgli_etl.pipeline_wrapper import PipelineWrapper


def test_sentic_pipeline(
    pipeline_storage,
    sentic_zip_url,
    full_sentic_zip_client,
    full_sentic_zip_owl_filename,
):
    argparse = ArgParser()
    SenticPipeline.add_arguments(argparse)

    args = argparse.parse_args(
        [
            "--sentic_zip_url",
            sentic_zip_url,
            "--owl_filename",
            full_sentic_zip_owl_filename,
        ]
    )
    pipeline_kwds = vars(args).copy()
    sentic_pipeline = SenticPipeline(
        http_client=full_sentic_zip_client, **pipeline_kwds
    )
    pipeline_wrapper = PipelineWrapper(sentic_pipeline, pipeline_storage)

    extract_kwds = pipeline_wrapper.extract()
    graph_generator = pipeline_wrapper.transform(**extract_kwds)

    nodes_by_id = {}
    primitive_ids = set()
    sentic_ids = set()
    edges_by_subject = {}
    for node_or_edge in graph_generator:
        if isinstance(node_or_edge, KgNode):
            node = node_or_edge
            nodes_by_id[node.id] = node
            type = node.id.split(":", 2)[1]
            if type == sentic_types.PRIMITIVE:
                primitive_ids.add(node.id)
            elif type == sentic_types.SENTIC:
                sentic_ids.add(node.id)
        elif isinstance(node_or_edge, KgEdge):
            edge = node_or_edge
            subject_edges = edges_by_subject.setdefault(edge.subject, [])
            subject_edges.append(node_or_edge)

    # assert that all concept nodes are related to sentics, primitives and other concepts
    for id, node in nodes_by_id.items():
        type = node.id.split(":", 2)[1]
        if type != sentic_types.CONCEPT:
            continue
        assert id in edges_by_subject
        concept_edges, primitive_edges, sentic_edges = [], [], []
        for edge in edges_by_subject[id]:
            if edge.object in primitive_ids:
                primitive_edges.append(edge)
            elif edge.object in sentic_ids:
                sentic_edges.append(edge)
            else:
                concept_edges.append(edge)
        assert len(concept_edges) > 0, node
        assert len(primitive_edges) > 0, node
        assert len(sentic_edges) > 0, node
