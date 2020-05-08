from typing import Generator, Union

from xml.dom.minidom import parse

from mowgli_etl.lib.cskg.concept_net_predicates import RELATED_TO
from mowgli_etl.lib.cskg.edge import Edge
from mowgli_etl.lib.cskg.node import Node
from mowgli_etl.lib.etl._transformer import _Transformer
from mowgli_etl.lib.etl.pipeline.sentic.sentic_constants import SENTIC_FILE_KEY
from mowgli_etl.lib.etl.pipeline.sentic.sentic_mappers import sentic_edge, sentic_node


class SENTICTransformer(_Transformer):
    def transform(self, **kwds) -> Generator[Union[Node, Edge], None, None]:

        self._logger.info("transform %s", SENTIC_FILE_KEY)

        with open(kwds[SENTIC_FILE_KEY], mode="r") as strength_file:
            # print(strength_file.read())
            dom = parse(strength_file)

            namedinds = dom.getElementsByTagName("owl:NamedIndividual")

            sentfields = (
                "pleasantness",
                "attention",
                "sensitivity",
                "aptitude",
                "polarity",
            )
            sentnodes = {
                sen: sentic_node(sen, other={"sentiment": True}) for sen in sentfields
            }

            for sen_node in sentnodes.values():
                yield sen_node

            for ind in namedinds:
                subjectword = ind.getAttribute("rdf:about").split("#")[-1]

                subjectnode = sentic_node(subjectword)

                semrows = ind.getElementsByTagName("semantics")

                if ind.hasChildNodes() == False:
                    continue

                childnames = {child.nodeName for child in ind.childNodes}

                for row in semrows:

                    targetword = row.getAttribute("rdf:resource").split("#")[-1]
                    targetnode = sentic_node(targetword)
                    edge = sentic_edge(subject=subjectnode, object_=targetnode)

                    yield subjectnode
                    yield targetnode
                    yield edge

                for sen in sentfields:
                    sent_value = ""

                    if sen not in childnames:
                        continue

                    sent_value = ind.getElementsByTagName(sen)[0].childNodes[0].data

                    sent_weight = float(sent_value)
                    sent_node = sentnodes[sen]
                    sent_edge = sentic_edge(
                        subject=subjectnode,
                        object_=sent_node,
                        weight=sent_weight,
                        predicate=RELATED_TO,
                    )

                    yield sent_edge
