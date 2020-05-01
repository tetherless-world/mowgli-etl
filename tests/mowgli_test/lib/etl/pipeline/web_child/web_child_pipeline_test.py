from mowgli.lib.etl.pipeline_wrapper import PipelineWrapper
from mowgli.lib.etl.web_child.web_child_pipeline import WebChildPipeline


def test_web_child_pipeline(
    pipeline_storage,
    part_whole_zip_url,
    part_whole_archive_filenames,
    wordnet_sense_url,
        web_child_test_http_client,
):
    pipeline = WebChildPipeline(
        http_client=web_child_test_http_client,
        part_whole_url=part_whole_zip_url,
        wordnet_sense_url=wordnet_sense_url,
        **part_whole_archive_filenames
    )
    pipeline_wrapper = PipelineWrapper(pipeline, pipeline_storage)
