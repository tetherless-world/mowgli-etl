from mowgli.lib.etl.pipeline_wrapper import PipelineWrapper
from mowgli.lib.etl.swow.swow_pipeline import SwowPipeline


def test_swow_pipeline(pipeline_storage, sample_archive_path, sample_swow_edges_path, sample_swow_nodes_path):
    args = {
        'swow_archive_path': sample_archive_path,
        'loader': 'cskg_csv'
    }
    swow_pipeline = SwowPipeline(**args)
    pipeline_wrapper = PipelineWrapper({}, swow_pipeline, pipeline_storage)

    extract_kwds = pipeline_wrapper.extract(force=True)
    graph_generator = pipeline_wrapper.transform(force=True, **extract_kwds)
    pipeline_wrapper.load(graph_generator)

    with open(pipeline_storage.loaded_data_dir_path / 'nodes.csv', mode='r') as nodes_file:
        nodes_file_contents = nodes_file.read()
        with open(sample_swow_nodes_path, mode='r') as sample_nodes_file:
            expected_nodes_file_contents = sample_nodes_file.read()
            assert nodes_file_contents == expected_nodes_file_contents

    with open(pipeline_storage.loaded_data_dir_path / 'edges.csv', mode='r') as edge_file:
        edge_file_contents = edge_file.read()
        with open(sample_swow_edges_path, mode='r') as sample_edge_file:
            expected_edge_file_contents = sample_edge_file.read()
            assert edge_file_contents == expected_edge_file_contents
