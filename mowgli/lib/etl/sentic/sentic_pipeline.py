from mowgli.lib.etl._pipeline import _Pipeline
from mowgli.lib.etl.sentic.sentic_extractor import SENTICExtractor
from mowgli.lib.etl.sentic.sentic_transformer import SENTICTransformer
from mowgli.lib.etl.sentic.sentic_constants import from_url
from mowgli.lib.etl.sentic.sentic_constants import sentic_archive_path
from mowgli.lib.etl.sentic.sentic_constants import sentic_target




class SenticPipeline(_Pipeline):

    def __init__(self,sentic_archive_path: str = sentic_archive_path,from_url=from_url, **kwds, ):
        _Pipeline.__init__(
            self,
            extractor=SENTICExtractor(
            from_url = kwds.get('sentic_from_url') if kwds.get('sentic_from_url') else from_url,
            target = kwds.get('target') if kwds.get('target') else sentic_target,
            http_client = kwds.get('http_client') if kwds.get('http_client') else None ),
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
            default=sentic_archive_path)

        arg_parser.add_argument(
            "--sentic-from-url",
            help="URL to zip file containing ontology data",
            required=False,
            default=from_url)

        
        arg_parser.add_argument(
            "--target",
            help="Base file name of file to be parsed",
            required=False,
            default=sentic_target)

        _Pipeline.add_arguments(arg_parser)

