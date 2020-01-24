from mowgli.lib.etl._pipeline import _Pipeline
from mowgli.lib.etl.eat.eat_extractor import EatExtractor
from mowgli.lib.etl.eat.eat_transformer import EatTransformer


class EatPipeline(_Pipeline):
    def __init__(self, xml_file_path: str):
        _Pipeline.__init__(
            self,
            extractor=EatExtractor(xml_file_path=xml_file_path),
            id="eat",
            transformer=EatTransformer()
        )

    @classmethod
    def add_arguments(cls, arg_parser):
        arg_parser.add_argument("--xml-file-path", help="EAT .xml file path")

