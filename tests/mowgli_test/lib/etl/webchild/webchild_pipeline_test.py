from mowgli.lib.etl.pipeline_wrapper import PipelineWrapper
from mowgli.lib.etl.webchild.webchild_pipeline import WebchildPipeline


def test_webchild_pipeline(
    pipeline_storage,
    part_whole_zip_url,
    part_whole_archive_filenames,
    wordnet_sense_url,
    webchild_test_http_client,
):
    pipeline = WebchildPipeline(
        http_client=webchild_test_http_client,
        part_whole_url=part_whole_zip_url,
        wordnet_sense_url=wordnet_sense_url,
        **part_whole_archive_filenames
    )
    pipeline_wrapper = PipelineWrapper(pipeline, pipeline_storage)
