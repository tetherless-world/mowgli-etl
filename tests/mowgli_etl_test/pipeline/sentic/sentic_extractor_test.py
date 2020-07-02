
from mowgli_etl.pipeline.sentic.sentic_constants import SENTIC_FILE_KEY
from mowgli_etl.pipeline.sentic.sentic_extractor import SENTICExtractor


def test_sentic_extractor(
    pipeline_storage,
    sample_sentic_file_path,
    sentic_zip_url,
    sample_sentic_zip_client,
    sample_sentic_zip_owl_filename,
):

    extractor = SENTICExtractor(
        sentic_zip_url=sentic_zip_url,
        owl_filename=sample_sentic_zip_owl_filename,
        http_client=sample_sentic_zip_client,
    )
    extraction = extractor.extract(force=False, storage=pipeline_storage)
    contents = open(extraction[SENTIC_FILE_KEY]).read()
    expected_contents = open(sample_sentic_file_path).read()
    assert contents == expected_contents
