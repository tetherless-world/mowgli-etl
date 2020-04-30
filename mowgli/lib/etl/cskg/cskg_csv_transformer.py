import csv
from pathlib import Path
from typing import Dict, Optional, Tuple

from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl._transformer import _Transformer


class CskgCsvTransformer(_Transformer):
    def transform(self, *, edges_csv_file_paths: Tuple[Path, ...], nodes_csv_file_paths: Tuple[Path, ...], **kwds):
        def get_optional_column(csv_row: Dict[str, str], column_name: str) -> Optional[str]:
            cell = csv_row.get(column_name)
            if cell is None:
                return
            cell = cell.strip()
            if not cell:
                return
            return cell

        def get_required_column(csv_row: Dict[str, str], column_name: str) -> Optional[str]:
            cell = csv_row[column_name]
            cell = cell.strip()
            if not cell:
                raise ValueError("missing value for column " + column_name)
            return cell

        for nodes_csv_file_path in nodes_csv_file_paths:
            self._logger.info("Reading CSKG nodes from %s", nodes_csv_file_path)
            with open(nodes_csv_file_path) as nodes_csv_file:
                csv_reader = csv.DictReader(nodes_csv_file, delimiter="\t", quoting=csv.QUOTE_NONE)
                for csv_row in csv_reader:
                    node = \
                        Node(
                            aliases=get_optional_column(csv_row, "aliases"),
                            datasource=get_required_column(csv_row, "datasource"),
                            id=get_required_column(csv_row, "id"),
                            label=get_optional_column(csv_row, "label"),
                            other=get_optional_column(csv_row, "other"),
                            pos=get_optional_column(csv_row, "pos"),
                        )
                    yield node

        for edges_csv_file_path in edges_csv_file_paths:
            self._logger.info("Reading CSKG edges from %s", edges_csv_file_path)
            with open(edges_csv_file_path) as edges_csv_file:
                csv_reader = csv.DictReader(edges_csv_file, delimiter="\t", quoting=csv.QUOTE_NONE)
                for csv_row in csv_reader:
                    # Edges may refer to nodes that are outside of the ones we've created e.g., WordNet.
                    yield \
                        Edge(
                            datasource=get_required_column(csv_row, "datasource"),
                            object_=get_required_column(csv_row, "object"),
                            other=csv_row.get("other"),
                            predicate=get_required_column(csv_row, "predicate"),
                            subject=get_required_column(csv_row, "subject"),
                            weight=float(get_required_column(csv_row, "weight"))
                        )
        self._logger.info("Finished transform.")
