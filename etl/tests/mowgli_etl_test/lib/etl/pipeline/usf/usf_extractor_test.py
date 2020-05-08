from mowgli_etl.lib.etl.pipeline.usf.usf_constants import STRENGTH_FILE_KEY
from mowgli_etl.lib.etl.pipeline.usf.usf_extractor import USFExtractor


def test_usf_extractor(pipeline_storage, strengths, url, usfclient):
    extractor = USFExtractor(
        http_client=usfclient,
        cue_target_url=url,
        cue_target_filename="usf_test_data-master/usf_test_data.xml",
    )
    extraction = extractor.extract(force=False, storage=pipeline_storage)
    with open(extraction[STRENGTH_FILE_KEY], mode="r") as strength_file:
        contents = strength_file.read()
        expected_contents = strengths.read()
        assert contents == expected_contents
