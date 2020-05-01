from mowgli.lib.etl._extractor import _Extractor
from mowgli.lib.etl.pipeline_storage import PipelineStorage
from mowgli.paths import DATA_DIR


class FoodOnExtractor(_Extractor):
    __FOOD_ON_OWL_BZ2_FILE_PATH = DATA_DIR / "food_on" / "extracted" / "food_on.owl.bz2"

    def extract(self, *, force: bool, storage: PipelineStorage):
        return {
            "food_on_owl_file_path": self._extract_bz2(force=force, path=self.__FOOD_ON_OWL_BZ2_FILE_PATH,
                                                       storage=storage)}
