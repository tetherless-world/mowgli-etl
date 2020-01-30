from mowgli.lib.etl._transformer import _Transformer
from mowgli.lib.cskg.node import Node
from mowgli.lib.cskg.edge import Edge
from mowgli.lib.etl.swow.swow_mappers import swow_edge, swow_node

from typing import Generator, Union
import csv

class SwowTransformer(_Transformer):
    """ 
    Transforms SWOW relations from a csv file into cskg nodes/edges.
    """

    def transform(self, *, csv_file_path: str) -> Generator[Union[Node, Edge], None, None]:
        """
        Generate nodes and edges from a SWOW strengths csv file.
        :param csv_file_path: path to SWOW strengths csv file
        """

        self._logger.info("transform %s", csv_file_path)
        with open(csv_file_path) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter='\t', quoting=csv.QUOTE_NONE)
            for row in csv_reader:
                cue = row['cue']
                response = row['response']
                strength = float(row['R123.Strength'])
                yield swow_node(cue)
                yield swow_node(response)
                yield swow_edge(cue=cue, response=response, strength=strength)
