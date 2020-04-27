import pytest

from mowgli.lib.etl.sentic.sentic_constants import SENTIC_FILE_KEY
from mowgli.lib.etl.sentic.sentic_extractor import SENTICExtractor


def test_sentic_extractor(pipeline_storage, strengths,url,senticclient):
    extractor = SENTICExtractor(sentic_zip_url= url, owl_filename="test_data-master/test_data.owl",http_client=senticclient)
    extraction = extractor.extract(force=False,storage = pipeline_storage)
    contents = open(extraction[SENTIC_FILE_KEY]).read()
    expected_contents = strengths.read()
    assert contents == expected_contents
