from mowgli.lib.etl._transformer import _Transformer
from mowgli.lib.cskg.node import Node
from mowgli.lib.cskg.edge import Edge
from typing import Generator, Union
from xml.dom.minidom import parse, parseString
from mowgli.lib.etl.sentic.sentic_constants import SENTIC_FILE_KEY
from mowgli.lib.etl.sentic.sentic_mappers import sentic_edge, sentic_node

class SENTICTransformer(_Transformer):
    def transform(self, **kwds) -> Generator[Union[Node, Edge], None, None]:


        self._logger.info("transform %s", SENTIC_FILE_KEY)
        

        with open(kwds[SENTIC_FILE_KEY], mode='r') as strength_file:
            #print(strength_file.read())
            dom = parse(strength_file)

            namedinds = dom.getElementsByTagName("owl:NamedIndividual")

            for ind in namedinds:
                subjectword = ind.getAttribute("rdf:about").split('#')[-1]

                subjectnode = sentic_node(subjectword)

                semrows = ind.getElementsByTagName("semantics")

                for row in semrows:

                    targetword = row.getAttribute("rdf:resource").split('#')[-1]
                    targetnode = sentic_node(targetword)
                    edge = sentic_edge(subject=subjectnode,object_=targetnode)

                    yield subjectnode
                    yield targetnode
                    yield edge

