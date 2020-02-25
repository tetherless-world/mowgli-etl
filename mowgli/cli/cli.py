import logging
import os.path
from importlib import import_module
from inspect import isclass
from typing import Generator, Union

from configargparse import ArgParser

from mowgli import paths
from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl._pipeline import _Pipeline
from mowgli.lib.etl.pipeline_storage import PipelineStorage


class Cli:
    class __PipelineWrapper:
        def __init__(self, args, logger, pipeline: _Pipeline):
            self.__args = args
            self.__logger = logger
            self.__pipeline = pipeline
            self.__storage = PipelineStorage(pipeline_id=pipeline.id, root_data_dir_path=self.__create_data_dir_path())

        def __create_data_dir_path(self) -> str:
            data_dir_path = self.__args.data_dir_path
            if data_dir_path is None:
                for data_dir_path in (
                        # In the container
                        "/data",
                        # In the checkout
                        paths.DATA_DIR
                ):
                    if os.path.isdir(data_dir_path):
                        break
            if not os.path.isdir(data_dir_path):
                raise ValueError("data dir path %s does not exist" % data_dir_path)
            data_dir_path = os.path.join(data_dir_path, self.__pipeline.id)
            if not os.path.isdir(data_dir_path):
                os.makedirs(data_dir_path)
                self.__logger.info("created pipeline data directory %s", data_dir_path)
            return data_dir_path

        def extract(self, force: bool):
            extract_kwds = self.__pipeline.extractor.extract(force=force, storage=self.__storage)
            return extract_kwds if extract_kwds is not None else {}

        def load(self, graph_generator: Generator[Union[Node, Edge], None, None]) -> None:
            with self.__pipeline.loader.open(storage=self.__storage) as loader:
                for node_or_edge in graph_generator:
                    if isinstance(node_or_edge, Node):
                        node = node_or_edge
                        loader.load_node(node_or_edge)
                    elif isinstance(node_or_edge, Edge):
                        loader.load_edge(node_or_edge)
                    else:
                        raise ValueError(type(node_or_edge))

        def transform(self, force: bool, **extract_kwds):
            return self.__pipeline.transformer.transform(**extract_kwds)

    def __init__(self):
        self.__arg_parser = ArgParser()
        self.__logger = logging.getLogger(self.__class__.__name__)

    def __add_arguments(self):
        self.__arg_parser.add_argument("-c", is_config_file=True, help="config file path")
        self.__arg_parser.add_argument("--data-dir-path",
                                       help="path to a directory to store extracted and transformed data")
        self.__arg_parser.add_argument(
            '--debug',
            action='store_true',
            help='turn on debugging'
        )
        self.__arg_parser.add_argument("-f", "--force", action="store_true",
                                       help="force extract and transform, ignoring any cached data")
        self.__arg_parser.add_argument("--force-extract", action="store_true",
                                       help="force extract, ignoring any cached data")
        self.__arg_parser.add_argument("--force-transform", action="store_true",
                                       help="force transform, ignoring any cached data")
        self.__arg_parser.add_argument("--fuseki-data-url", default="http://fuseki:3030/ds/data")
        self.__arg_parser.add_argument(
            '--logging-level',
            help='set logging-level level (see Python logging module)'
        )
        self.__arg_parser.add_argument(
            '--pipeline-module',
            help='absolute (parent.module) or relative (.module) module name for the pipeline implementation',
            required=True
        )

    def __configure_logging(self, args):
        if args.debug:
            logging_level = logging.DEBUG
        elif args.logging_level is not None:
            logging_level = getattr(logging, args.logging_level.upper())
        else:
            logging_level = logging.INFO
        logging.basicConfig(
            format='%(asctime)s:%(module)s:%(lineno)s:%(name)s:%(levelname)s: %(message)s',
            level=logging_level
        )

    def __import_pipeline_class(self, args) -> _Pipeline:
        try_pipeline_module_names = [args.pipeline_module]
        if not "." in args.pipeline_module:
            try_pipeline_module_names.append(".%s.%s" % (args.pipeline_module, args.pipeline_module + "_pipeline"))

        first_import_error = None
        pipeline_module = None
        for pipeline_module_name_i, pipeline_module_name in enumerate(try_pipeline_module_names):
            try:
                pipeline_module = import_module(pipeline_module_name, _Pipeline.__module__.rsplit(".", 1)[0])
                break
            except ImportError as e:
                if pipeline_module_name_i == 0:
                    first_import_error = e

        if pipeline_module is None:
            raise first_import_error

        for attr in dir(pipeline_module):
            value = getattr(pipeline_module, attr)
            if isclass(value) and issubclass(value, _Pipeline):
                return value
        raise ImportError("no Pipeline in the %s module" % pipeline_module.__name__)

    def __instantiate_pipeline(self, args, pipeline_class, **kwds) -> _Pipeline:
        pipeline_kwds = vars(args).copy()
        pipeline_kwds.pop("c")
        pipeline_kwds.pop("data_dir_path")
        pipeline_kwds.pop("force")
        pipeline_kwds.pop("force_extract")
        pipeline_kwds.pop("force_transform")
        pipeline_kwds.pop("logging_level")
        pipeline_kwds.pop("pipeline_module")
        pipeline_kwds.update(kwds)
        return pipeline_class(**pipeline_kwds)

    def main(self):
        self.__add_arguments()
        args, _ = self.__arg_parser.parse_known_args()
        self.__configure_logging(args)

        pipeline_class = self.__import_pipeline_class(args)
        pipeline_class.add_arguments(self.__arg_parser)

        args = self.__arg_parser.parse_args()

        pipeline = self.__instantiate_pipeline(args, pipeline_class)
        pipeline_wrapper = self.__PipelineWrapper(args=args, logger=self.__logger, pipeline=pipeline)

        force = bool(getattr(args, "force", False))
        force_extract = force or bool(getattr(args, "force_extract", False))
        force_transform = force or bool(getattr(args, "force_transform", False))

        extract_kwds = pipeline_wrapper.extract(force=force_extract)
        graph_generator = pipeline_wrapper.transform(force=force_transform, **extract_kwds)
        pipeline_wrapper.load(graph_generator)


def main():
    Cli().main()


if __name__ == '__main__':
    main()
