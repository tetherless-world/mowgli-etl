from mowgli_etl._pipeline import _Pipeline
from mowgli_etl.pipeline.eat.eat_extractor import EatExtractor
from mowgli_etl.pipeline.eat.eat_transformer import EatTransformer
from mowgli_etl.paths import DATA_DIR

default_eat_file_path = str(DATA_DIR / 'eat' / 'eat100.xml')


class EatPipeline(_Pipeline):
    def __init__(self, xml_file_path: str = default_eat_file_path, **kwds):
        _Pipeline.__init__(
            self,
            extractor=EatExtractor(xml_file_path=xml_file_path),
            id="eat",
            transformer=EatTransformer(),
            **kwds
        )

    @classmethod
    def add_arguments(cls, arg_parser):
        _Pipeline.add_arguments(arg_parser)
        arg_parser.add_argument("--xml-file-path", help="EAT .xml file path", default=default_eat_file_path)

