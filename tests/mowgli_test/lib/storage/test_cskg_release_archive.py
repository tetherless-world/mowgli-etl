from mowgli import paths
from mowgli.lib.storage.cskg_release_archive import CskgReleaseArchive

if (paths.DATA_DIR / "cskg_release" / "extracted").is_dir():
    def test_constructon():
        with CskgReleaseArchive() as archive:
            pass


    def test_open_nodes_csv():
        with CskgReleaseArchive() as archive:
            with archive.open_nodes_csv("conceptnet") as nodes_csv_file:
                pass
