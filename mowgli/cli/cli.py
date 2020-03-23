import logging
import sys

from configargparse import ArgParser

from mowgli.cli.commands.drive_upload_command import DriveUploadCommand
from mowgli.cli.commands.etl_command import EtlCommand


class Cli(object):
    def __init__(self):
        self.__commands = {
            "etl": EtlCommand(),
            "drive-upload": DriveUploadCommand(),
        }

    def __configure_logging(self, args):
        if args.debug:
            logging_level = logging.DEBUG
        elif args.logging_level is not None:
            logging_level = getattr(logging, args.logging_level.upper())
        else:
            logging_level = logging.INFO
        logging.basicConfig(
            format="%(asctime)s:%(module)s:%(lineno)s:%(name)s:%(levelname)s: %(message)s",
            level=logging_level,
        )

    def main(self):
        arg_parser = ArgParser()
        args = self.__parse_args(arg_parser)
        self.__configure_logging(args)
        args.command(args, arg_parser)

    def __parse_args(self, arg_parser: ArgParser):
        arg_parser.add_argument("-c", is_config_file=True, help="config file path")
        arg_parser.add_argument(
            "--debug", action="store_true", help="turn on debugging"
        )
        arg_parser.add_argument(
            "--logging-level",
            help="set logging-level level (see Python logging module)",
        )
        subparsers = arg_parser.add_subparsers()
        for command_name, command in self.__commands.items():
            subparser = subparsers.add_parser(command_name)
            command.add_arguments(subparser)
            subparser.set_defaults(command=command)

        parsed_args = arg_parser.parse_args()

        if not hasattr(parsed_args, "command"):
            arg_parser.print_usage()
            sys.exit(1)

        return parsed_args


def main():
    Cli().main()
