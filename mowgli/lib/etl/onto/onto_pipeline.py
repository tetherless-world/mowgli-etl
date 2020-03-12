from mowgli.lib.etl._pipeline import _Pipeline
from mowgli.lib.etl.onto.onto_extractor import ONTOExtractor
from mowgli.lib.etl.onto.onto_transformer import ONTOTransformer
from mowgli.lib.etl.onto.onto_constants import from_url
from mowgli.lib.etl.onto.onto_constants import onto_archive_path
from mowgli.lib.etl.onto.onto_constants import onto_target




class OntoPipeline(_Pipeline):

    def __init__(self,onto_archive_path: str = onto_archive_path,from_url=from_url, **kwds, ):
        _Pipeline.__init__(
            self,
            extractor=ONTOExtractor(onto_archive_path=onto_archive_path, from_url = from_url),
            id = "onto",
            transformer=ONTOTransformer(),
            **kwds
        )

    @classmethod
    def add_arguments(cls, arg_parser):
        _Pipeline.add_arguments(arg_parser)
        arg_parser.add_argument(
            "--onto-archive-path",
            help="Path to a zip archive to use as a source of ONTO data",
            required=False,
            default=onto_archive_path)

        _Pipeline.add_arguments(arg_parser)
        arg_parser.add_argument(
            "--onto-from-url",
            help="url to zip",
            required=False,
            default=from_url)

        _Pipeline.add_arguments(arg_parser)
        arg_parser.add_argument(
            "--target",
            help="url to zip",
            required=False,
            default=onto_target)



