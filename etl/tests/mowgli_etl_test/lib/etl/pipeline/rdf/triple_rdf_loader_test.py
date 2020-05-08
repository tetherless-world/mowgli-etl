import pytest
import rdflib

from mowgli_etl.lib.cskg.edge import Edge
from mowgli_etl.lib.etl.pipeline.rdf.triple_rdf_loader import TripleRdfLoader
from mowgli_etl.lib.etl.pipeline_storage import PipelineStorage
from mowgli_etl.lib.etl.pipeline_wrapper import PipelineWrapper
from tests.mowgli_etl_test.lib.etl.pipeline.rdf.rdf_loader_test_pipeline import RdfLoaderTestPipeline


@pytest.fixture
def pipeline(cskg_edges_csv_file_path, cskg_nodes_csv_file_path,
             pipeline_storage: PipelineStorage):
    return PipelineWrapper(pipeline=RdfLoaderTestPipeline(cskg_edges_csv_file_path=cskg_edges_csv_file_path,
                                                          cskg_nodes_csv_file_path=cskg_nodes_csv_file_path,
                                                          loader="triple_rdf_ttl"),
                           storage=pipeline_storage)


def test_load(pipeline: PipelineWrapper, pipeline_storage: PipelineStorage):
    pipeline.run()
    ttl_file_path = pipeline_storage.loaded_data_dir_path / (
            pipeline.id + ".ttl")
    graph = rdflib.Graph()
    graph.parse(format="trig",
                source=str(ttl_file_path))
    assert len(graph)


def test_load_missing_node(pipeline_storage: PipelineStorage):
    with TripleRdfLoader(format="ttl", pipeline_id="test").open(pipeline_storage) as loader:
        loader.load_edge(Edge(
            datasource="test",
            object="missing_object",
            predicate="predicate",
            subject="missing_subject",
        ))
