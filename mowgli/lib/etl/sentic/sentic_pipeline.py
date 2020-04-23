from mowgli.lib.etl._pipeline import _Pipeline
from mowgli.lib.etl.sentic.sentic_extractor import SENTICExtractor
from mowgli.lib.etl.sentic.sentic_transformer import SENTICTransformer
from mowgli.lib.etl.sentic.sentic_constants import ONTOSENTICNET_ZIP_URL
from mowgli.lib.etl.sentic.sentic_constants import SENTIC_ARCHIVE_PATH
from mowgli.lib.etl.sentic.sentic_constants import ONTOSENTICNET_OWL_FILENAME




class SenticPipeline(_Pipeline):

    def __init__(self, sentic_archive_path: str = SENTIC_ARCHIVE_PATH, from_url=ONTOSENTICNET_ZIP_URL, **kwds, ):
        _Pipeline.__init__(
            self,
            extractor=SENTICExtractor(from_url = kwds['sentic_from_url'],target = kwds['target']),
            id = "sentic",
            transformer=SENTICTransformer(),
            **kwds
        )

    @classmethod
    def add_arguments(cls, arg_parser):
        arg_parser.add_argument(
            "--sentic-archive-path",
            help="Path to a zip archive to use as a source of SENTIC data",
            required=False,
            default=SENTIC_ARCHIVE_PATH)

        arg_parser.add_argument(
            "--sentic-from-url",
            help="URL to zip file containing ontology data",
            required=False,
            default=ONTOSENTICNET_ZIP_URL)

        
        arg_parser.add_argument(
            "--target",
            help="Base file name of file to be parsed",
            required=False,
            default=ONTOSENTICNET_OWL_FILENAME)

        _Pipeline.add_arguments(arg_parser)

