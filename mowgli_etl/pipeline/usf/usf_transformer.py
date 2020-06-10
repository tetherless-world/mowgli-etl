from typing import Generator, Union

from xml.dom.minidom import parse

from mowgli_etl.model.edge import Edge
from mowgli_etl.model.node import Node
from mowgli_etl._transformer import _Transformer
from mowgli_etl.pipeline.usf.usf_constants import STRENGTH_FILE_KEY
from mowgli_etl.pipeline.usf.usf_mappers import usf_edge, usf_node

""" 
The frequency attribute refers to a score of natural frequency of said
word in the English language based on a 1967 study (Kucera and Francis),
which is widely regarded as the standard source for said metric.
Ranking scored from least common (0) to most common (9999).

Read more: http://crr.ugent.be/papers/Brysbaert%20&%20New%20BRM%202009%20Subtlexus.pdf

The concreteness attribute refers to the tangiblity of an item's referant.
The concreteness rating of a word based on its level
of abstraction from from abstract (1) to concrete (7).
(Paivio, Yuille, & Madigan, 1968; Toglia & Battig, 1978)

Read more: http://datavis.ca/papers/twp.pdf

"""


class USFTransformer(_Transformer):

    def transform(self, **kwds) -> Generator[Union[Node, Edge], None, None]:

        self._logger.info("transform %s", STRENGTH_FILE_KEY)

        with open(kwds[STRENGTH_FILE_KEY], mode='r') as strength_file:
            dom = parse(strength_file)

            cue = dom.getElementsByTagName('cue')

            for cuetag in cue:
                cuenode = self.buildnode(cuetag)
                targettag = cuetag.getElementsByTagName('target')

                for target in targettag:
                    targetnode = self.buildnode(target)

                    yield cuenode
                    yield targetnode
                    yield usf_edge(cue=cuenode, response=targetnode, strength=float(target.getAttribute("fsg")))

    def buildnode(self,element) -> usf_node:
        word = element.getAttribute("word")
        pos = element.getAttribute("pos")
        tag = element.getElementsByTagName('target')
        otherdict = dict()
        if element.hasAttribute("fr"):
            otherdict['frequency'] = int(element.getAttribute("fr"))
        if element.hasAttribute("con"):
            otherdict['concreteness'] = float(element.getAttribute("con"))

        return usf_node(cueOrResponse=word,pos= pos,other=otherdict)
