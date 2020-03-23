import logging
from abc import ABC, abstractmethod
from configargparse import ArgParser


class _Command(ABC):
    """
    A command-line (sub-)command.
    For each _Command, the command-line entrypoint (main):
    1) Creates an ArgumentParser sub-command parser
    2) Calls .add_arguments to add sub-command specific arguments to this sub-parser
    If the sub-command is invoked, then
    3) Invoke .__call__ with the parsed arguments and the arg parser
    """

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    def add_arguments(self, arg_parser: ArgParser) -> None:
        """
        Add sub-command-specific arguments to the argparse (sub-) ArgParser
        """

    @abstractmethod
    def __call__(self, args, arg_parser: ArgParser) -> None:
        """
        Invoke .__call__ with the parsed arguments and the arg parser
        """
