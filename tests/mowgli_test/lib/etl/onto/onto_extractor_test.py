from mowgli.lib.etl.onto.onto_extractor import ONTOExtractor
from mowgli.lib.etl.onto.onto_constants import STRENGTH_FILE_KEY
from xml.dom.minidom import parse, parseString
from mowgli.lib.etl.onto.onto_constants import onto_archive_path



def test_onto_extractor(pipeline_storage, strengths,url):
    extractor = ONTOExtractor(onto_archive_path=strengths, from_url = url)
    extraction = extractor.extract(force=False,storage = pipeline_storage, target = "test_data.owl")
    contents = open(extraction[STRENGTH_FILE_KEY]).read()
    expected_contents = strengths.read()
    assert contents == expected_contents

