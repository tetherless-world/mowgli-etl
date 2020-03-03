import pytest
import rdflib

from mowgli.lib.etl.pipeline_storage import PipelineStorage
from mowgli.lib.etl.pipeline_wrapper import PipelineWrapper
from tests.mowgli_test.lib.etl.rdf.rdf_loader_test_pipeline import RdfLoaderTestPipeline

_EXPECTED_NODE_HEADER = 'id\tlabel\taliases\tpos\tdatasource\tother'
_EXPECTED_EDGE_HEADER = 'subject\tpredicate\tobject\tdatasource\tweight\tother'


@pytest.fixture
def pipeline(cskg_edges_csv_file_path, cskg_nodes_csv_file_path,
             pipeline_storage: PipelineStorage):
    return PipelineWrapper(pipeline=RdfLoaderTestPipeline(cskg_edges_csv_file_path=cskg_edges_csv_file_path,
                                                          cskg_nodes_csv_file_path=cskg_nodes_csv_file_path,
                                                          loader="quad-rdf-trig"),
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
