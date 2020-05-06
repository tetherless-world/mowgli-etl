import logging

from configargparse import ArgParser

from mowgli.cli.commands.augment_cskg_release_command import AugmentCskgReleaseCommand
from mowgli.cli.commands.drive_upload_command import DriveUploadCommand
from mowgli.cli.commands.etl_command import EtlCommand
try:
    from mowgli.cli.commands.index_concept_net_command import IndexConceptNetCommand
except ImportError:
    IndexConceptNetCommand = None


class Cli:
    def __init__(self):
        self.__commands = {
            "augment-cskg-release": AugmentCskgReleaseCommand(),
            "etl": EtlCommand(),
            "drive-upload": DriveUploadCommand()
        }
        if IndexConceptNetCommand is not None:
            self.__commands["index-concept-net"] = IndexConceptNetCommand()

    @staticmethod
    def __add_global_args(arg_parser: ArgParser):
        arg_parser.add_argument("-c", is_config_file=True, help="config file path")
        arg_parser.add_argument(
            "--debug", action="store_true", help="turn on debugging"
        )
        arg_parser.add_argument(
            "--logging-level",
            help="set logging-level level (see Python logging module)",
        )

    def __configure_logging(self, args):
        if args.debug:
            logging_level = logging.DEBUG
        elif args.logging_level is not None:
            logging_level = getattr(logging, args.logging_level.upper())
        else:
            logging_level = logging.INFO
        logging.basicConfig(
            format="%(asctime)s:%(processName)s:%(module)s:%(lineno)s:%(name)s:%(levelname)s: %(message)s",
            level=logging_level,
        )

    def main(self):
        args = self.__parse_args()
        self.__configure_logging(args)
        self.__commands[args.command](args)

    def __parse_args(self):
        arg_parser = ArgParser()
        subparsers = arg_parser.add_subparsers(
            title="commands", dest="command"
        )
        self.__add_global_args(arg_parser)
        for command_name, command in self.__commands.items():
            subparser = subparsers.add_parser(command_name)
            self.__add_global_args(subparser)
            command.add_arguments(subparser, self.__add_global_args)

        parsed_args = arg_parser.parse_args()

        return parsed_args


def main():
    Cli().main()


if __name__ == "__main__":
    main()
