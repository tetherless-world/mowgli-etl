from pathlib import Path

import pytest
import rdflib

from mowgli.lib.etl._pipeline import _Pipeline
from mowgli.lib.etl.cskg.cskg_csv_extractor import CskgCsvExtractor
from mowgli.lib.etl.cskg.cskg_csv_transformer import CskgCsvTransformer
from mowgli.lib.etl.pipeline_storage import PipelineStorage
from mowgli.lib.etl.pipeline_wrapper import PipelineWrapper

_EXPECTED_NODE_HEADER = 'id\tlabel\taliases\tpos\tdatasource\tother'
_EXPECTED_EDGE_HEADER = 'subject\tpredicate\tobject\tdatasource\tweight\tother'


class QuadRdfLoaderTestPipeline(_Pipeline):
    def __init__(self, *, cskg_edges_csv_file_path: Path, cskg_nodes_csv_file_path: Path):
        _Pipeline.__init__(
            self,
            extractor=CskgCsvExtractor(edges_csv_file_paths=(cskg_edges_csv_file_path,),
                                       nodes_csv_file_paths=(cskg_nodes_csv_file_path,)),
            id="quad_rdf_loader_test",
            loader="quad-rdf-trig",
            transformer=CskgCsvTransformer(),
        )


@pytest.fixture
def quad_rdf_loader_test_pipeline_wrapper(cskg_edges_csv_file_path, cskg_nodes_csv_file_path,
                                          pipeline_storage: PipelineStorage):
    return PipelineWrapper(pipeline=QuadRdfLoaderTestPipeline(cskg_edges_csv_file_path=cskg_edges_csv_file_path,
                                                              cskg_nodes_csv_file_path=cskg_nodes_csv_file_path),
                           storage=pipeline_storage)


def test_load(quad_rdf_loader_test_pipeline_wrapper: PipelineWrapper, pipeline_storage: PipelineStorage):
    extract_result = quad_rdf_loader_test_pipeline_wrapper.extract()
    transform_result = quad_rdf_loader_test_pipeline_wrapper.transform(**extract_result)
    quad_rdf_loader_test_pipeline_wrapper.load(transform_result)
    trig_file_path = pipeline_storage.loaded_data_dir_path / (
            quad_rdf_loader_test_pipeline_wrapper.id + ".trig")
    conjunctive_graph = rdflib.ConjunctiveGraph()
    conjunctive_graph.parse(format="trig",
                            source=str(trig_file_path))
    # conjunctive_graph.serialize(format="trig")
    have_context = False
    for context in conjunctive_graph.contexts():
        have_context = True
        assert len(context)
    assert have_context
