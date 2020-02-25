from mowgli.lib.etl.usf.usf_extractor import USFExtractor
from mowgli.lib.etl.usf.usf_constants import STRENGTH_FILE_KEY
from xml.dom.minidom import parse, parseString


def test_usf_extractor(pipeline_storage, strengths,url):
    extractor = USFExtractor()
    extraction = extractor.extract(force=False,storage = pipeline_storage, url = url, target = "usf_test_data.xml")
    contents = extraction[STRENGTH_FILE_KEY].read()
    expected_contents = strengths.read()
    assert contents == expected_contents
