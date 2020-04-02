from mowgli.lib.etl._transformer import _Transformer
from mowgli.lib.cskg.node import Node
from mowgli.lib.cskg.edge import Edge
from mowgli.lib.etl.usf.usf_mappers import usf_edge, usf_node
from typing import Generator, Union
from xml.dom.minidom import parse, parseString
from mowgli.lib.etl.usf.usf_constants import STRENGTH_FILE_KEY


class USFTransformer(_Transformer):

    def transform(self, **kwds) -> Generator[Union[Node, Edge], None, None]:

        self._logger.info("transform %s", STRENGTH_FILE_KEY)

        with open(kwds[STRENGTH_FILE_KEY], mode='r') as strength_file:
            dom = parse(strength_file)

            cue = dom.getElementsByTagName('cue')

            for cuetag in cue:
                cueword = cuetag.getAttribute("word")
                cuepos = cuetag.getAttribute("pos")
                targettag = cuetag.getElementsByTagName('target')
                cueotherdict = dict()
                try:
                    cueotherdict['fr'] = int(cuetag.getAttribute("fr"))
                except:
                    pass
                try:
                    cueotherdict['con'] = float(cuetag.getAttribute("con"))
                except:
                    pass

                cuenode = usf_node(cueword, cuepos,cueotherdict)

                for target in targettag:
                    targetword = target.getAttribute("word")
                    targetpos = target.getAttribute("pos")
                    targetotherdict = dict()
                    try:
                        targetotherdict['fr'] = int(target.getAttribute("fr"))
                    except:
                        pass
                    try:
                        targetotherdict['con'] = float(target.getAttribute("con"))
                    except:
                        pass

                    targetnode = usf_node(targetword, targetpos,targetotherdict)
            
                    yield cuenode
                    yield targetnode
                    yield usf_edge(cue=cuenode, response=targetnode, strength=float(target.getAttribute("fsg")))
