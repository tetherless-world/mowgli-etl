from mowgli.lib.etl._transformer import _Transformer
from mowgli.lib.cskg.node import Node
from mowgli.lib.cskg.edge import Edge
from typing import Generator, Union
from xml.dom.minidom import parse, parseString
from mowgli.lib.etl.sentic.sentic_constants import SENTIC_FILE_KEY, sentiment
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
                
                pleas_value = ""
                try:
                    pleas_value=ind.getElementsByTagName("pleasantness")[0].childNodes[0].data
                except:
                    continue

                
                pleas_weight = float(pleas_value)
                pleas_node = sentic_node("pleasantness")
                please_edge = sentic_edge(subject=subjectnode,object_=pleas_node,weight=pleas_weight,predicate=sentiment)

                yield please_edge

                att_value = ind.getElementsByTagName("attention")[0].childNodes[0].data

                att_weight = float(att_value)
                att_node = sentic_node("attention")
                att_edge = sentic_edge(subject=subjectnode,object_=att_node,weight=att_weight,predicate=sentiment)

                yield att_edge

                sens_value = ind.getElementsByTagName("sensitivity")[0].childNodes[0].data
                sens_weight = float(sens_value)
                sens_node = sentic_node("sensitivity")
                sens_edge = sentic_edge(subject=subjectnode,object_=sens_node,weight=sens_weight,predicate=sentiment)
            

                yield sens_edge

                apt_value =  ind.getElementsByTagName("aptitude")[0].childNodes[0].data
                apt_weight = float(apt_value)
                apt_node = sentic_node("aptitude")
                apt_edge = sentic_edge(subject=subjectnode,object_=apt_node,weight=apt_weight,predicate=sentiment)

                yield apt_edge

                pol_value = ind.getElementsByTagName("polarity")[0].childNodes[0].data
                pol_weight = float(pol_value)
                pol_node = sentic_node("polarity")
                pol_edge = sentic_edge(subject=subjectnode,object_=pol_node,weight=pol_weight,predicate=sentiment)

                yield pol_edge


