from mowgli.lib.etl._transformer import _Transformer
from mowgli.lib.cskg.node import Node
from mowgli.lib.cskg.edge import Edge
from typing import Generator, Union
from xml.dom.minidom import parse, parseString
from mowgli.lib.etl.onto.onto_constants import STRENGTH_FILE_KEY
from mowgli.lib.etl.onto.onto_mappers import onto_edge, onto_node

class ONTOTransformer(_Transformer):
    def transform(self, **kwds) -> Generator[Union[Node, Edge], None, None]:


        self._logger.info("transform %s", STRENGTH_FILE_KEY)
        

        with open(kwds[STRENGTH_FILE_KEY], mode='r') as strength_file:
            #print(strength_file.read())
            dom = parse(strength_file)

            namedinds = dom.getElementsByTagName("owl:NamedIndividual")

            for ind in namedinds:
                cueword = ind.getAttribute("rdf:about").split('#')[-1]

                cuenode = onto_node(cueword)

                semrows = ind.getElementsByTagName("semantics")

                for row in semrows:

                    targetword = row.getAttribute("rdf:resource").split('#')[-1]
                    targetnode = onto_node(targetword)
                    edge = onto_edge(cue=cuenode,response=targetnode)

                    yield cuenode
                    yield targetnode
                    yield edge

