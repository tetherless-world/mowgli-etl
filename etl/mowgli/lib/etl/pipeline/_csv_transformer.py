from typing import Dict, Optional

from mowgli.lib.etl._transformer import _Transformer


class _CsvTransformer(_Transformer):
    @staticmethod
    def _get_optional_column(csv_row: Dict[str, str], column_name: str) -> Optional[str]:
        cell = csv_row.get(column_name)
        if cell is None:
            return
        cell = cell.strip()
        if not cell:
            return
        return cell

    @staticmethod
    def _get_required_column(csv_row: Dict[str, str], column_name: str) -> Optional[str]:
        cell = csv_row[column_name]
        cell = cell.strip()
        if not cell:
            raise ValueError("missing value for column " + column_name)
        return cell
