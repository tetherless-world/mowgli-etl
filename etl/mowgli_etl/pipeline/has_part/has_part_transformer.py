import json
from pathlib import Path
from typing import Generator, Set, Dict
from urllib.parse import quote

from mowgli_etl.cskg.concept_net_predicates import HAS_A, PART_OF
from mowgli_etl.cskg.edge import Edge
from mowgli_etl.cskg.mowgli_predicates import SAME_AS
from mowgli_etl.cskg.node import Node
from mowgli_etl._transformer import _Transformer
from mowgli_etl.word_net_id import WordNetId


class HasPartTransformer(_Transformer):
    __DATASOURCE = "has_part"

    def __convert_normalized_arg_to_node(self, normalized_arg):
        # Create nodes in a custom namespace.
        # Will do sameAs WordNet or Wikipedia nodes in the transform instead of reusing their id's here.
        # Don't include metadata as "other", since the data set contains multiple normalized args with different metadata,
        # which violates our duplicate node id checks.
        metadata = normalized_arg.get("metadata", {})
        if "synset" in metadata:
            synset = metadata["synset"]
            assert synset.startswith("wn.")
            word_net_id = WordNetId.parse(synset[len("wn."):])
            pos = word_net_id.pos
        else:
            pos = None

        label = normalized_arg["normalized"]
        id_ = f"{self.__DATASOURCE}:{quote(label)}"
        if pos is not None:
            id_ += ":" + pos

        return \
            Node(
                datasource=self.__DATASOURCE,
                id=id_,
                label=label,
                pos=pos,
                # other=normalized_arg.get("metadata")
            )

    def transform(self, has_part_kb_jsonl_file_path: Path):
        same_as_edges_yielded = {}

        with open(has_part_kb_jsonl_file_path, "r") as has_part_kb_jsonl_file:
            for line in has_part_kb_jsonl_file:
                json_object = json.loads(line)

                arg1_object = json_object["arg1"]
                arg1_node = self.__convert_normalized_arg_to_node(arg1_object)
                yield arg1_node

                arg2_object = json_object["arg2"]
                arg2_node = self.__convert_normalized_arg_to_node(arg2_object)
                yield arg2_node

                yield from \
                    self.__yield_has_part_edges(
                        arg1_node=arg1_node,
                        arg2_node=arg2_node,
                        average_score=json_object["average_score"]
                    )

                yield from \
                    self.__yield_same_as_edges(
                        arg1_node=arg1_node,
                        arg1_object=arg1_object,
                        arg2_node=arg2_node,
                        arg2_object=arg2_object,
                        same_as_edges_yielded=same_as_edges_yielded
                    )

    def __yield_has_part_edges(self, *, arg1_node: Node, arg2_node: Node, average_score: float) -> Generator[
        Edge, None, None]:
        # arg1 HasA arg2
        yield Edge(
            datasource=self.__DATASOURCE,
            subject=arg1_node.id,
            object=arg2_node.id,
            predicate=HAS_A,
            weight=average_score,
        )

        # Inverse, arg2 PartOf arg2
        yield Edge(
            datasource=self.__DATASOURCE,
            subject=arg2_node.id,
            object=arg1_node.id,
            predicate=PART_OF,
            weight=average_score,
        )

    def __yield_same_as_edges(self, *, arg1_node: Node, arg1_object, arg2_node: Node, arg2_object,
                              same_as_edges_yielded: Dict[str, Set[str]]) -> Generator[
        Edge, None, None]:
        for arg_node, arg_object in (
                (arg1_node, arg1_object),
                (arg2_node, arg2_object),
        ):
            metadata = arg_object.get("metadata")
            if metadata is None:
                continue

            node_same_as_edges_yielded = same_as_edges_yielded.get(arg_node.id)
            if node_same_as_edges_yielded is None:
                same_as_edges_yielded[arg_node.id] = node_same_as_edges_yielded = set()

            if "synset" in metadata:
                synset = metadata["synset"]
                assert synset.startswith("wn.")
                wn_node_id = "wn:" + synset[len("wn."):]
                if wn_node_id in node_same_as_edges_yielded:
                    continue
                yield Edge(
                    datasource=self.__DATASOURCE,
                    object=wn_node_id,
                    predicate=SAME_AS,
                    subject=arg_node.id,
                )
                node_same_as_edges_yielded.add(wn_node_id)

            if "wikipedia_primary_page" in metadata:
                wikipedia_primary_page = metadata["wikipedia_primary_page"]
                wikipedia_node_id = "wikipedia:" + quote(wikipedia_primary_page)
                if wikipedia_node_id in node_same_as_edges_yielded:
                    continue
                yield Edge(
                    datasource=self.__DATASOURCE,
                    object=wikipedia_node_id,
                    predicate=SAME_AS,
                    subject=arg_node.id,
                )
                node_same_as_edges_yielded.add(wikipedia_node_id)
