import json
from pathlib import Path
from urllib.parse import quote

from mowgli.lib.cskg.concept_net_predicates import HAS_A, PART_OF
from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.mowgli_predicates import SAME_AS
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl._transformer import _Transformer


class HasPartTransformer(_Transformer):
    __DATASOURCE = "hasPartKB"

    def __normalized_arg_to_node(self, normalized_arg):
        # Create nodes in a custom namespace.
        # Will do sameAs WordNet or Wikipedia nodes in the transform instead of reusing their id's here.
        return \
            Node(
                datasource=self.__DATASOURCE,
                id=self.__DATASOURCE + ":" + quote(normalized_arg["normalized"]),
                label=normalized_arg["normalized"],
                other=normalized_arg.get("metadata")
            )

    def transform(self, has_part_kb_jsonl_file_path: Path):
        with open(has_part_kb_jsonl_file_path, "r") as has_part_kb_jsonl_file:
            for line in has_part_kb_jsonl_file:
                json_object = json.loads(line)
                arg1_node = self.__normalized_arg_to_node(json_object["arg1"])
                arg2_node = self.__normalized_arg_to_node(json_object["arg2"])
                average_score = json_object["average_score"]

                # arg1 HasA arg2
                yield Edge(
                    datasource=self.__DATASOURCE,
                    subject=arg1_node,
                    object_=arg2_node,
                    predicate=HAS_A,
                    weight=average_score,
                )

                # Inverse, arg2 PartOf arg2
                yield Edge(
                    datasource=self.__DATASOURCE,
                    subject=arg2_node,
                    object_=arg1_node,
                    predicate=PART_OF,
                    weight=average_score,
                )

                for node in (arg1_node, arg2_node):
                    metadata = node.other
                    if metadata is None:
                        continue
                    if "synset" in metadata:
                        synset = metadata["synset"]
                        assert synset.startswith("wn.")
                        yield Edge(
                            datasource=self.__DATASOURCE,
                            object_=Node(
                                datasource=self.__DATASOURCE,
                                id="wn:" + synset[len("wn."):],
                                label=node.label,
                            ),
                            predicate=SAME_AS,
                            subject=node,
                        )
                    if "wikipedia_primary_page" in metadata:
                        wikipedia_primary_page = metadata["wikipedia_primary_page"]
                        yield Edge(
                            datasource=self.__DATASOURCE,
                            object_=Node(
                                datasource=self.__DATASOURCE,
                                id="wikipedia:" + wikipedia_primary_page,
                                label=node.label,
                            ),
                            predicate=SAME_AS,
                            subject=node,
                        )
