from typing import Optional, List

from mowgli_etl.lib.etl._pipeline import _Pipeline
from mowgli_etl.lib.etl.pipeline.cskg_csv.cskg_csv_extractor import CskgCsvExtractor
from mowgli_etl.lib.etl.pipeline.cskg_csv.cskg_csv_transformer import CskgCsvTransformer


class RdfPipeline(_Pipeline):
    def __init__(self, *, edges_csv_file_paths: List[str],
                 nodes_csv_file_paths: List[str], pipeline_id: str, loader: Optional[str] = None, **kwds):
        _Pipeline.__init__(
            self,
            extractor=CskgCsvExtractor(edges_csv_file_paths=edges_csv_file_paths,
                                       nodes_csv_file_paths=nodes_csv_file_paths),
            id=pipeline_id,
            loader=loader if loader is not None else "triple_rdf_ttl",
            transformer=CskgCsvTransformer(),
            **kwds
        )

    @classmethod
    def add_arguments(cls, arg_parser):
        arg_parser.add_argument("--pipeline-id", required=True)
        CskgCsvExtractor.add_arguments(arg_parser)
