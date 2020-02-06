from mowgli.lib.etl._transformer import _Transformer
from mowgli.lib.cskg.node import Node
from mowgli.lib.cskg.edge import Edge
from mowgli.lib.etl.webchild.webchild_mappers import webchild_edge, webchild_node

from typing import Generator, Union
import csv

class webchildTransformer(_Transformer):
    """ 
    Transforms webchild relations from a csv file into cskg nodes/edges.
    """

    def transform(self, *, webchild_csv_file_paths: list) -> Generator[Union[Node, Edge], None, None]:
        """
        Generate nodes and edges from a webchild csv file.
        :param csv_file_path: path to webchild csv file
        """
        for csv_file_path in webchild_csv_file_paths:
            self._logger.info("transform %s", csv_file_path)      
            f = open(csv_file_path, "r")
            for x in f:
                info = x.split('\t')
                if('WordNetWrapper' in csv_file_path):
                    cue_node = webchild_node(info[0])
                    response_node = webchild_node(info[3])
                else:
                    cue_node = webchild_node(info[1])
                    response_node = webchild_node(info[4])
                yield cue_node
                yield response_node
                #DO i want to make the change for "part of" here rather in mappers file. 
                yield webchild_edge(cue=cue_node, response=response_node,csvPath =csv_file_path)

