import pytest

from mowgli.lib.etl.sentic.sentic_extractor import SENTICExtractor
from mowgli.lib.etl.sentic.sentic_constants import SENTIC_FILE_KEY
from xml.dom.minidom import parse, parseString
from mowgli.lib.etl.sentic.sentic_constants import SENTIC_ARCHIVE_PATH


@pytest.mark.skip(reason="Depends on external resource that has since been changed")
def test_sentic_extractor(pipeline_storage, strengths,url):
    extractor = SENTICExtractor(from_url = url,target = "test_data.owl")
    extraction = extractor.extract(force=False,storage = pipeline_storage)
    contents = open(extraction[SENTIC_FILE_KEY]).read()
    expected_contents = strengths.read()
    assert contents == expected_contents

