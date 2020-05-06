from pathlib import Path

from mowgli.lib.etl._pipeline import _Pipeline
from mowgli.lib.etl.pipeline.cskg_csv.cskg_csv_extractor import CskgCsvExtractor
from mowgli.lib.etl.pipeline.cskg_csv.cskg_csv_transformer import CskgCsvTransformer


class RdfLoaderTestPipeline(_Pipeline):
    def __init__(self, *, cskg_edges_csv_file_path: Path, cskg_nodes_csv_file_path: Path, loader: str):
        _Pipeline.__init__(
            self,
            extractor=CskgCsvExtractor(edges_csv_file_paths=(cskg_edges_csv_file_path,),
                                       nodes_csv_file_paths=(cskg_nodes_csv_file_path,)),
            id="quad_rdf_loader_test",
            loader=loader,
            transformer=CskgCsvTransformer(),
        )
