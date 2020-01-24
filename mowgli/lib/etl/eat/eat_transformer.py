from mowgli.lib.etl._transformer import _Transformer


class EatTransformer(_Transformer):
    def transform(self, xml_file_path: str):
        self._logger.info("transform %s", xml_file_path)
        # Yield Nodes and Edges
        raise NotImplementedError
