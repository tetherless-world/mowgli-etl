from mowgli.lib.etl._pipeline import _Pipeline
from mowgli.lib.etl.sentic.sentic_constants import ONTOSENTICNET_OWL_FILENAME
from mowgli.lib.etl.sentic.sentic_constants import ONTOSENTICNET_ZIP_URL
from mowgli.lib.etl.sentic.sentic_extractor import SENTICExtractor
from mowgli.lib.etl.sentic.sentic_transformer import SENTICTransformer
from mowgli.lib.etl.sentic.sentic_constants import from_url
from mowgli.lib.etl.sentic.sentic_constants import sentic_archive_path
from mowgli.lib.etl.sentic.sentic_constants import sentic_target


class SenticPipeline(_Pipeline):
    def __init__(
        self,
        *,
        sentic_zip_url=ONTOSENTICNET_ZIP_URL,
        owl_filename=ONTOSENTICNET_OWL_FILENAME,
        **kwds
    ):
        _Pipeline.__init__(
            self,
            extractor=SENTICExtractor(
                http_client=kwds.get("http_client")
                if kwds.get("http_client")
                else None,
                sentic_zip_url=sentic_zip_url, 
                owl_filename=owl_filename
            ),
            id="sentic",
            transformer=SENTICTransformer(),
            **kwds,
        )

    @classmethod
    def add_arguments(cls, arg_parser):
        arg_parser.add_argument(
            "--sentic_zip_url",
            help="URL to zip file containing ontology data",
            required=False,
            default=ONTOSENTICNET_ZIP_URL,
        )
        arg_parser.add_argument(
            "--owl_filename",
            help="Name of the OntoSenticNet OWL file within the sentic zip archive.",
            required=False,
            default=ONTOSENTICNET_OWL_FILENAME,
        )
        _Pipeline.add_arguments(arg_parser)
