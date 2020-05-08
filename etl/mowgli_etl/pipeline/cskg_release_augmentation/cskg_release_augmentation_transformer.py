from pathlib import Path

from mowgli_etl.lib.etl._transformer import _Transformer


class CskgReleaseAugmentationTransformer(_Transformer):
    def transform(self, *, cskg_release_zip_file_path: Path, rpi_combined_edges_csv_file_path: Path,
                  rpi_combined_nodes_csv_file_path: Path):
        pass
