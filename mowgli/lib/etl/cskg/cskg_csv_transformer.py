import csv
from pathlib import Path
from typing import Dict, Optional

from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl._transformer import _Transformer


class CskgCsvTransformer(_Transformer):
    def transform(self, extracted_data_dir_path: Path, **kwds):
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

        nodes_by_id = {}
        with open(extracted_data_dir_path / "nodes.csv") as nodes_csv_file:
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
                # assert node.id not in nodes_by_id, node.id
                nodes_by_id[node.id] = node

        with open(extracted_data_dir_path / "edges.csv") as edges_csv_file:
            csv_reader = csv.DictReader(edges_csv_file, delimiter="\t", quoting=csv.QUOTE_NONE)
            for csv_row in csv_reader:
                subject = nodes_by_id[get_required_column(csv_row, "subject")]
                object_ = nodes_by_id[get_required_column(csv_row, "object")]

                yield \
                    Edge(
                        datasource=get_required_column(csv_row, "datasource"),
                        object_=object_,
                        other=csv_row.get("other"),
                        relation=get_required_column(csv_row, "predicate"),
                        subject=subject,
                        weight=float(get_required_column(csv_row, "weight"))
                    )
