from urllib.parse import quote

from xml.dom.minidom import parse

from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.model.kg_node import KgNode
from mowgli_etl._transformer import _Transformer


class EatTransformer(_Transformer):
    def transform(self, xml_file_path: str):
        self._logger.info("transform %s", xml_file_path)
        # Yield Nodes and Edges

        dom = parse(xml_file_path)

        stimuli = dom.getElementsByTagName('stimulus')

        for stimulus in stimuli:
            stim_word = str(stimulus.attributes['word'].value)
            stim_node = KgNode(datasource="eat", id="eat:" + quote(stim_word), label=stim_word)
            yield stim_node

            responses = stimulus.getElementsByTagName('response')

            for response in responses:
                response_word = str(response.attributes['word'].value)
                percent = float(response.attributes['r'].value)
                response_node = KgNode(datasource="eat", id="eat:" + quote(response_word), label=response_word)
                yield response_node
                yield KgEdge(datasource="eat", object=stim_node.id, predicate="cn:RelatedTo", subject=response_node.id,
                           weight=percent)
