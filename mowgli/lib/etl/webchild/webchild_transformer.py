from mowgli.lib.etl._transformer import _Transformer
from mowgli.lib.cskg.node import Node
from mowgli.lib.cskg.edge import Edge
from mowgli.lib.etl.webchild.webchild_constants import WEBCHILD_MEMBEROF_DATASOURCE_ID, WEBCHILD_PHYSICAL_DATASOURCE_ID,WEBCHILD_NAMESPACE, WEBCHILD_WORD_NET_WRAPPER
from mowgli.lib.cskg.concept_net_predicates import HAS_A, PART_OF, DEFINED_AS,MADE_OF

from typing import Generator, Union
import csv

class WebchildTransformer(_Transformer):

    def __transform_physical_csv(physical_csv_file_path:str) -> Generator[Union[Node, Edge], None, None]:
        
        datasource = WEBCHILD_PHYSICAL_DATASOURCE_ID
        relation = PART_OF
        with open(physical_csv_file_path) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter='\t', quoting=csv.QUOTE_NONE)
            for row in csv_reader:
                object1_node = Node(datasource=datasource, id="webchild:" + row['to_ss'], label=row['to_word'])
                object2_node = Node(datasource=datasource, id="webchild:" + row['from_ss'], label=row['from_word'])
                yield object1_node
                yield object2_node
                #I think subject indicates the second object 
                yield Edge(datasource=datasource, object_=object1_node, relation=relation, subject=object2_node)

    
    def __transform_memberof_csv(memberof_csv_file_path:str) -> Generator[Union[Node, Edge], None, None]:
    
        datasource = WEBCHILD_MEMBEROF_DATASOURCE_ID
        relation = HAS_A
        with open(memberof_csv_file_path) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter='\t', quoting=csv.QUOTE_NONE)
            for row in csv_reader:
                object1_node = Node(datasource=datasource, id="webchild:" + row['to_ss'], label=row['to_word'])
                object2_node = Node(datasource=datasource, id="webchild:" + row['from_ss'], label=row['from_word'])
                yield object1_node
                yield object2_node
                #I think subject indicates the second object 
                yield Edge(datasource=datasource, object_=object1_node, relation=relation, subject=object2_node)

    def __transform_substanceof_csv(self, *, substanceof_csv_file_path: str) -> Generator[Union[Node, Edge], None, None]:
        
        datasource = WEBCHILD_SUBSTANCEOF_DATASOURCE_ID
        relation = MADE_OF
        with open(substanceof_csv_file_path) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter='\t', quoting=csv.QUOTE_NONE)
            for row in csv_reader:
                object1_node = Node(datasource=WEBCHILD_SUBSTANCEOF_DATASOURCE_ID, id="webchild:" + row['to_ss'], label=row['to_word'])
                object2_node = Node(datasource=WEBCHILD_SUBSTANCEOF_DATASOURCE_ID, id="webchild:" + row['from_ss'], label=row['from_word'])
                yield object1_node
                yield object2_node
                #I think subject indicates the second object 
                yield Edge(datasource=datasource, object_=object1_node, relation=relation, subject=object2_node)

    def __transform_wordnet_csv(self, *, substanceof_csv_file_path: str) -> Generator[Union[Node, Edge], None, None]:
        
        datasource = WEBCHILD_WORD_NET_WRAPPER
        relation = DEFINED_AS
        with open(substanceof_csv_file_path) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter='\t', quoting=csv.QUOTE_NONE)
            for row in csv_reader:
                object1_node = Node(datasource=WEBCHILD_WORD_NET_WRAPPER, id="webchild:" + row['WordNet-synsetid'], label=row['#word'])
                object2_node = Node(datasource=WEBCHILD_WORD_NET_WRAPPER, id="webchild:" + row['WordNet-synsetid'], label=row['Definition (WordNet gloss)'])
                yield object1_node
                yield object2_node
                #I think subject indicates the second object 
                yield Edge(datasource=datasource, object_=object1_node, relation=relation, subject=object2_node)



    def transform(self, *, memberof_csv_file_path: str, physical_csv_file_path: str, substanceof_csv_file_path:str, wordnet_csv_file_path:str):
        yield from __transform_memberof_csv(memberof_csv_file_path)
        yield from __transform_physical_csv(physical_csv_file_path)
        yield from __transform_substanceof_csv(physical_csv_file_path)
        yield from __transform_wordnet_csv(wordnet_csv_file_path)


    

        
