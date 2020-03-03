from pathlib import Path

import pytest

from mowgli.lib.etl._pipeline import _Pipeline
from mowgli.lib.etl.cskg.cskg_csv_extractor import CskgCsvExtractor
from mowgli.lib.etl.cskg.cskg_csv_transformer import CskgCsvTransformer
from mowgli.lib.etl.pipeline_storage import PipelineStorage
from mowgli.lib.etl.pipeline_wrapper import PipelineWrapper
from mowgli.lib.etl.rdf.rdf_loader import RdfLoader

_EXPECTED_NODE_HEADER = 'id\tlabel\taliases\tpos\tdatasource\tother'
_EXPECTED_EDGE_HEADER = 'subject\tpredicate\tobject\tdatasource\tweight\tother'


class RdfLoaderTestPipeline(_Pipeline):
    def __init__(self, cskg_edges_csv_file_path: Path, cskg_nodes_csv_file_path: Path):
        _Pipeline.__init__(
            extractor=CskgCsvExtractor(edges_csv_file_paths=(cskg_edges_csv_file_path,),
                                       nodes_csv_file_paths=(cskg_nodes_csv_file_path,)),
            id="rdf_loader_test",
            loader=RdfLoader(),
            transformer=CskgCsvTransformer(),
        )


@pytest.fixture
def rdf_loader_test_pipeline_wrapper(cskg_edges_csv_file_path, cskg_nodes_csv_file_path,
                                     pipeline_storage: PipelineStorage):
    return PipelineWrapper(pipeline=RdfLoaderTestPipeline(cskg_edges_csv_file_path=cskg_edges_csv_file_path,
                                                          cskg_nodes_csv_file_path=cskg_nodes_csv_file_path),
                           storage=pipeline_storage)


def test_load(rdf_loader_test_pipeline_wrapper: PipelineWrapper, pipeline_storage: PipelineStorage):
    extract_result = rdf_loader_test_pipeline_wrapper.extract()
    transform_result = rdf_loader_test_pipeline_wrapper.transform(**extract_result)
    rdf_loader_test_pipeline_wrapper.load()
