from mowgli.lib.etl._transformer import _Transformer
from mowgli.lib.cskg.node import Node
from mowgli.lib.cskg.edge import Edge
from typing import Generator, Union
from xml.dom.minidom import parse, parseString
from mowgli.lib.etl.sentic.sentic_constants import SENTIC_FILE_KEY
from mowgli.lib.etl.sentic.sentic_mappers import sentic_edge, sentic_node
from mowgli.lib.cskg.concept_net_predicates import RELATED_TO

class SENTICTransformer(_Transformer):
    def transform(self, **kwds) -> Generator[Union[Node, Edge], None, None]:


        self._logger.info("transform %s", SENTIC_FILE_KEY)
        

        with open(kwds[SENTIC_FILE_KEY], mode='r') as strength_file:
            #print(strength_file.read())
            dom = parse(strength_file)

            namedinds = dom.getElementsByTagName("owl:NamedIndividual")

            sents_yielded = False

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
                
                
                sentfields = ("pleasantness","attention", "sensitivity", "aptitude","polarity")

                for sen in sentfields:
                    sent_value = ""
                    try:
                        sent_value=ind.getElementsByTagName(sen)[0].childNodes[0].data
                    except:
                        continue

                    sent_weight = float(sent_value)
                    sent_node = sentic_node(sen)
                    sent_edge = sentic_edge(subject=subjectnode,object_=sent_node,weight=sent_weight,predicate=RELATED_TO)
                   
                    if sents_yielded == False:
                        yield sent_node
                    yield sent_edge


                sents_yielded = True



