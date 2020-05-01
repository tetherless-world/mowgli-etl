from pathlib import Path
from typing import Tuple

from mowgli.lib.etl._transformer import _Transformer
from mowgli.lib.etl.pipeline.cskg.cskg_edges_csv_transformer import CskgEdgesCsvTransformer
from mowgli.lib.etl.pipeline.cskg.cskg_nodes_csv_transformer import CskgNodesCsvTransformer


class CskgCsvTransformer(_Transformer):
    def transform(self, *, edges_csv_file_paths: Tuple[Path, ...], nodes_csv_file_paths: Tuple[Path, ...], **kwds):
        for nodes_csv_file_path in nodes_csv_file_paths:
            self._logger.info("Reading CSKG nodes from %s", nodes_csv_file_path)
            yield from CskgNodesCsvTransformer().transform(nodes_csv_file=nodes_csv_file_path)

        for edges_csv_file_path in edges_csv_file_paths:
            self._logger.info("Reading CSKG edges from %s", edges_csv_file_path)
            yield from CskgEdgesCsvTransformer().transform(edges_csv_file=edges_csv_file_path)
        self._logger.info("Finished transform.")
