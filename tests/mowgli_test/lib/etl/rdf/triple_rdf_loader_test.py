import pytest
import rdflib

from mowgli.lib.etl.pipeline_storage import PipelineStorage
from mowgli.lib.etl.pipeline_wrapper import PipelineWrapper
from tests.mowgli_test.lib.etl.rdf.rdf_loader_test_pipeline import RdfLoaderTestPipeline


@pytest.fixture
def pipeline(cskg_edges_csv_file_path, cskg_nodes_csv_file_path,
             pipeline_storage: PipelineStorage):
    return PipelineWrapper(pipeline=RdfLoaderTestPipeline(cskg_edges_csv_file_path=cskg_edges_csv_file_path,
                                                          cskg_nodes_csv_file_path=cskg_nodes_csv_file_path,
                                                          loader="triple_rdf_ttl"),
                           storage=pipeline_storage)


def test_load(pipeline: PipelineWrapper, pipeline_storage: PipelineStorage):
    pipeline.extract_transform_load()
    ttl_file_path = pipeline_storage.loaded_data_dir_path / (
            pipeline.id + ".ttl")
    graph = rdflib.Graph()
    graph.parse(format="trig",
                source=str(ttl_file_path))
    assert len(graph)
