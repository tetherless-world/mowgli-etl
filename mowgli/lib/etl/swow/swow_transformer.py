<<<<<<< HEAD
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
                cue_node = swow_node(row['cue'])
                response_node = swow_node(row['response'])
                strength = float(row['R123.Strength'])
                yield cue_node
                yield response_node
                yield swow_edge(cue=cue_node, response=response_node, strength=strength)
=======
import csv
from typing import Generator, Union

from mowgli.lib.cskg.node import Node
from mowgli.lib.cskg.edge import Edge
from mowgli.lib.etl.swow.swow_constants import STRENGTH_FILE_KEY
from mowgli.lib.etl.swow.swow_mappers import swow_edge, swow_node
from mowgli.lib.etl._transformer import _Transformer


class SwowTransformer(_Transformer):
    """ 
    Transforms SWOW relations from a csv file into cskg nodes/edges.
    """

    def transform(self, **kwds) -> Generator[Union[Node, Edge], None, None]:
        """
        Generate nodes and edges from a SWOW strengths csv file.
        :param csv_file: SWOW strengths csv file
        """
        if STRENGTH_FILE_KEY not in kwds:
            raise ValueError(f'No SWOW strengths file found for key {STRENGTH_FILE_KEY}')
        csv_file = kwds[STRENGTH_FILE_KEY]
        csv_reader = csv.DictReader(csv_file, delimiter='\t', quoting=csv.QUOTE_NONE)
        for row in csv_reader:
            cue_node = swow_node(row['cue'])
            response_node = swow_node(row['response'])
            strength = float(row['R123.Strength'])
            yield cue_node
            yield response_node
            yield swow_edge(cue=cue_node, response=response_node, strength=strength)
>>>>>>> f528e6b5c73c4cc8f9bf8dff32ab4079085d3fde
