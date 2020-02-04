from mowgli.lib.etl._transformer import _Transformer
from mowgli.lib.cskg.node import Node
from mowgli.lib.cskg.edge import Edge
#from mowgli.lib.etl.swow.swow_mappers import swow_edge, swow_node
from mowgli.lib.etl.usf.usf_mappers import usf_edge, usf_node
from typing import Generator, Union
from xml.dom.minidom import parse, parseString

class USFTransformer(_Transformer):


    def transform(self, *, xml_file_path: str) -> Generator[Union[Node, Edge], None, None]:



        self._logger.info("transform %s", xml_file_path)

        dom = parse(xml_file_path)

        cue = dom.getElementsByTagName('cue')

        for cuetag in cue:
            cueword = cuetag.getAttribute("word")
            cuepos = cuetag.getAttribute("pos")
            targettag = cuetag.getElementsByTagName('target')

            cuenode = usf_node(cueword,cuepos)

            for target in targettag:
                targetword = target.getAttribute("word")
                targetpos = target.getAttribute("pos")
                targetnode = usf_node(targetword,targetpos)

                yield cuenode
                yield targetnode
                yield usf_edge(cue=cuenode,response=targetnode, strength=float(target.getAttribute("fsg")) )
            


         