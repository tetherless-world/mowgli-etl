from mowgli.lib.etl._transformer import _Transformer
from mowgli.lib.cskg.node import Node
from mowgli.lib.cskg.edge import Edge

from typing import Generator, Union
import csv

class WebchildTransformer(_Transformer):

    #helper functino to identify datasource and relation based off of 
    def find_proper_data_source_id(csv_path:str) -> str:
        if('memberof' in csv_path):
            return WEBCHILD_MEMEBEROF_DATASOURCE_ID,HAS_A
        if('physical' in csv_path):
            return WEBCHILD_PHYSICAL_DATASOURCE_ID,PART_OF
        if('substanceof' in csv_path):
            return WEBCHILD_SUBSTANCEOF_DATASOURCE_ID,MADE_OF
        if('WordNetWrapper' in csv_path):
            return WEBCHILD_WORD_NET_WRAPPER,DEFINED_AS


    def transform(self, *, webchild_csv_file_paths: list) -> Generator[Union[Node, Edge], None, None]:
        """
        Generate nodes and edges from a webchild csv file.
        """
        for csv_file_path in webchild_csv_file_paths:
            self._logger.info("transform %s", csv_file_path)      
            file = open(csv_file_path, "r")
            for line in file:
                info = line.split('\t')
                if('WordNetWrapper' in csv_file_path):
                    object1_node = Node(datasource="webchild", id="webchild:" + info[0], label=info[0])
                    object2_node = Node(datasource="webchild", id="webchild:" + info[3], label=info[3])
                elif('physical' in csv_file_path):
                #switch which object is which node
                    object1_node = Node(datasource="webchild", id="webchild:" + info[3], label=info[4])
                    object2_node = Node(datasource="webchild", id="webchild:" + info[0], label=info[1])
                else:
                    object1_node = Node(datasource="webchild", id="webchild:" + info[0], label=info[1])
                    object2_node = Node(datasource="webchild", id="webchild:" + info[3], label=info[4])
                
                datasource,relation = find_proper_data_source_id(csvPath = csv_file_path)
                yield object1_node
                yield object2_node
                #I think subject indicates the second object 
                yield Edge(datasource=datasource, object_=object1_node, relation=relation, subject=object2_node)
