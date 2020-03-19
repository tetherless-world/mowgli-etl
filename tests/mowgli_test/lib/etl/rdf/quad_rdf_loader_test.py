import pytest
import rdflib

from mowgli.lib.cskg.edge import Edge
from mowgli.lib.etl.pipeline_storage import PipelineStorage
from mowgli.lib.etl.pipeline_wrapper import PipelineWrapper
from mowgli.lib.etl.rdf.quad_rdf_loader import QuadRdfLoader
from tests.mowgli_test.lib.etl.rdf.rdf_loader_test_pipeline import RdfLoaderTestPipeline


@pytest.fixture
def pipeline(cskg_edges_csv_file_path, cskg_nodes_csv_file_path,
             pipeline_storage: PipelineStorage):
    return PipelineWrapper(pipeline=RdfLoaderTestPipeline(cskg_edges_csv_file_path=cskg_edges_csv_file_path,
                                                          cskg_nodes_csv_file_path=cskg_nodes_csv_file_path,
                                                          loader="quad_rdf_trig"),
                           storage=pipeline_storage)


def test_load(pipeline: PipelineWrapper, pipeline_storage: PipelineStorage):
    pipeline.extract_transform_load()
    trig_file_path = pipeline_storage.loaded_data_dir_path / (
            pipeline.id + ".trig")
    conjunctive_graph = rdflib.ConjunctiveGraph()
    conjunctive_graph.parse(format="trig",
                            source=str(trig_file_path))
    # conjunctive_graph.serialize(format="trig")
    have_context = False
    for context in conjunctive_graph.contexts():
        have_context = True
        assert len(context)
    assert have_context


def test_load_missing_node(pipeline_storage: PipelineStorage):
    with QuadRdfLoader(format="ttl", pipeline_id="test").open(pipeline_storage) as loader:
        loader.load_edge(Edge(
            datasource="test",
            object_="missing_object",
            predicate="predicate",
            subject="missing_subject",
        ))
