import csv
from pathlib import Path
from typing import Union, TextIO, Generator

from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.pipeline._csv_transformer import _CsvTransformer


class CskgEdgesCsvTransformer(_CsvTransformer):
    def transform(self, *, edges_csv_file: Union[Path, TextIO]) -> Generator[KgEdge, None, None]:
        if isinstance(edges_csv_file, Path):
            edges_csv_file_path = edges_csv_file
            with open(edges_csv_file_path) as edges_csv_file:
                yield from self.__transform(edges_csv_file=edges_csv_file)
        else:
            yield from self.__transform(edges_csv_file=edges_csv_file)

    def __transform(self, edges_csv_file: TextIO) -> Generator[KgEdge, None, None]:
        csv_reader = csv.DictReader(edges_csv_file, delimiter="\t", quoting=csv.QUOTE_NONE)
        for csv_row in csv_reader:
            # Edges may refer to nodes that are outside of the ones we've created e.g., WordNet.
            yield \
                KgEdge.legacy(
                    datasource=self._get_required_column(csv_row, "datasource"),
                    object=self._get_required_column(csv_row, "object"),
                    other=csv_row.get("other"),
                    predicate=self._get_required_column(csv_row, "predicate"),
                    subject=self._get_required_column(csv_row, "subject"),
                    weight=float(self._get_required_column(csv_row, "weight"))
                )
