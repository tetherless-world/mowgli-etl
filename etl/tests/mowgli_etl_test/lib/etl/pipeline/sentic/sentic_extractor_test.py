from pathlib import Path

from mowgli_etl.lib.etl.pipeline.sentic.sentic_constants import SENTIC_FILE_KEY
from mowgli_etl.lib.etl.pipeline.sentic.sentic_extractor import SENTICExtractor


def test_sentic_extractor(pipeline_storage, strengths, url, senticclient):
    extractor = SENTICExtractor(sentic_zip_url=url, owl_filename=str(Path(__file__).parent / "test_data.owl"),
                                http_client=senticclient)
    extraction = extractor.extract(force=False, storage=pipeline_storage)
    contents = open(extraction[SENTIC_FILE_KEY]).read()
    expected_contents = strengths.read()
    assert contents == expected_contents
