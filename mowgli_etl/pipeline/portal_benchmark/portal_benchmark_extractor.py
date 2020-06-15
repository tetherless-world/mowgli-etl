from mowgli_etl._extractor import _Extractor


class PortalBenchmarkExtractor(_Extractor):
    def extract(self, *, storage, **kwds):
        return {
            "kagnet_commonsenseqa_benchmark_submission_jsonl_bz2_file_path": storage.extracted_data_dir_path / "kagnet" / "commonsenseqa" / "dev_set_concept_pair_path_attention_scores.jsonl.bz2"
        }
