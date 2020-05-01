from pathlib import Path

from mowgli.lib.etl.pipeline.web_child.web_child_extractor import WebChildExtractor


def test_web_child_extractor(
    pipeline_storage,
    part_whole_zip_url,
    part_whole_archive_filenames,
    wordnet_sense_url,
        web_child_test_http_client,
):
    extractor = WebChildExtractor(
        http_client=web_child_test_http_client,
        part_whole_url=part_whole_zip_url,
        wordnet_sense_url=wordnet_sense_url,
        **part_whole_archive_filenames
    )

    extraction = extractor.extract(force=False, storage=pipeline_storage)

    expected_extraction_keys = (
        "memberof_csv_file_path",
        "physical_csv_file_path",
        "substanceof_csv_file_path",
        "wordnet_csv_file_path",
    )

    for key in expected_extraction_keys:
        assert key in extraction
        assert Path(extraction[key]).exists()
