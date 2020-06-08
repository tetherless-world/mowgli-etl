import os.path

from mowgli_etl.pipeline.food_on.food_on_extractor import FoodOnExtractor


def test_food_on_extractor(pipeline_storage):
    result = FoodOnExtractor().extract(force=False, storage=pipeline_storage)
    assert len(result) == 1
    file_path = result["food_on_owl_file_path"]
    assert os.path.dirname(file_path) == str(pipeline_storage.extracted_data_dir_path)
    assert os.path.exists(file_path)
