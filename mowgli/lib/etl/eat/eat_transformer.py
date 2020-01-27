from mowgli.lib.etl._transformer import _Transformer


class EatTransformer(_Transformer):
    def transform(self, xml_file_path: str):
        self._logger.info("transform %s", xml_file_path)
        # Yield Nodes and Edges

        dom = parse(xml_file_path)

        stimuli = dom.getElementsByTagName('stimulus')

        for stimulus in stimuli:
            stim_word = str(stimulus.attributes['word'].value)
            stim_node = Node(datasource="eat", id="eat:" + stim_word, label=stim_word)
            yield stim_node

            responses = stimulus.getElementsByTagName('response')

            for response in responses:
                response_word = str(response.attributes['word'].value)
                response_node = Node(datasource="eat", id="eat:" + response_word, label=response_word)
                yield response_node

        yield Edge(datasource="eat", object=stim_node, relation="cn:RelatedTo", subject=response_node)

        raise NotImplementedError