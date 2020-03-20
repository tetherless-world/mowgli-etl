from mowgli.lib.etl.onto.onto_extractor import ONTOExtractor
from mowgli.lib.etl.onto.onto_constants import ONTOLOGY_FILE_KEY
from xml.dom.minidom import parse, parseString
from mowgli.lib.etl.onto.onto_constants import onto_archive_path



def test_onto_extractor(pipeline_storage, strengths,url):
    extractor = ONTOExtractor(from_url = url,target = "test_data.owl")
    extraction = extractor.extract(force=False,storage = pipeline_storage)
    contents = open(extraction[ONTOLOGY_FILE_KEY]).read()
    expected_contents = strengths.read()
    assert contents == expected_contents

