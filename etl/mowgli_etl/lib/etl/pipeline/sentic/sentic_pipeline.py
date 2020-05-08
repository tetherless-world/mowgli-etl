from mowgli_etl.lib.etl._pipeline import _Pipeline
from mowgli_etl.lib.etl.pipeline.sentic.sentic_constants import ONTOSENTICNET_OWL_FILENAME
from mowgli_etl.lib.etl.pipeline.sentic.sentic_constants import ONTOSENTICNET_ZIP_URL
from mowgli_etl.lib.etl.pipeline.sentic.sentic_extractor import SENTICExtractor
from mowgli_etl.lib.etl.pipeline.sentic.sentic_transformer import SENTICTransformer


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
                sentic_zip_url=sentic_zip_url,
                owl_filename=owl_filename,
                **kwds
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
