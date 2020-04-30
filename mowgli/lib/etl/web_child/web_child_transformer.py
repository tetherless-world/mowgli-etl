import csv
from pathlib import Path
from typing import Dict, Generator, Tuple, Union

from mowgli.lib.cskg.concept_net_predicates import HAS_A, MADE_OF, PART_OF
from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.mowgli_predicates import WN_SYNSET
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl._transformer import _Transformer


class WebChildTransformer(_Transformer):

    # Mapping of WebChild relations to their equivalent conceptnet relation
    # and a boolean indicating whether the equivalent relation is inverted.
    __RELATION_DICT = {
        "hasMember": (HAS_A, False),
        "hasPart": (PART_OF, True),
        "hasSubstance": (MADE_OF, False),
    }
    __DATASOURCE_ID = "WebChild"
    __NAMESPACE = "WebChild"

    def __webchild_nid(self, ssid: str):
        return f"{self.__NAMESPACE}:{ssid}"

    def __webchild_node(self, *, ssid: str, word: str) -> Node:
        return Node(
            datasource=self.__DATASOURCE_ID,
            id=self.__webchild_nid(ssid),
            label=word,
            # All subjects/objects are nouns in WebChild part-whole
            pos="n",
        )

    def __read_webchild_csv_row(self, row: dict) -> Tuple[Node, Node, Edge]:
        subject_node = self.__webchild_node(ssid=row["to_ss"], word=row["to_word"])
        object_node = self.__webchild_node(ssid=row["from_ss"], word=row["from_word"])

        relation, inverted = self.__RELATION_DICT[row["relation"]]
        if inverted:
            subject_node, object_node = object_node, subject_node
        other = {
            "isvisual": row["isvisual"] == "v",
            "cardinality": row["cardinality"].strip(),
        }
        score = float(row["score"])
        edge = Edge(
            datasource=self.__DATASOURCE_ID,
            object=object_node.id,
            predicate=relation,
            subject=subject_node.id,
            other=other,
            weight=score,
        )
        return subject_node, object_node, edge

    def __transform_webchild_file(
        self, *, csv_file_path: Path, yielded_words: Dict[str, Node]
    ) -> Generator[Union[Node, Edge], None, None]:
        self._logger.info("transforming %s", csv_file_path)
        with open(csv_file_path) as csv_file:
            csv_reader = csv.DictReader(
                csv_file, delimiter="\t", quoting=csv.QUOTE_NONE
            )
            for row in csv_reader:
                subject_node, object_node, edge = self.__read_webchild_csv_row(row)
                for node in (subject_node, object_node):
                    if node.id not in yielded_words:
                        yield node
                        yielded_words[node.id] = node.label
                yield edge

    def __transform_wordnet_csv(
        self, *, wordnet_csv_file_path: Path, yielded_words: Dict[str, Node]
    ) -> Generator[Union[Node, Edge], None, None]:
        self._logger.info("transforming wordnet mappings from %s", wordnet_csv_file_path)
        with open(wordnet_csv_file_path) as csv_file:
            csv_reader = csv.DictReader(
                csv_file, delimiter="\t", quoting=csv.QUOTE_NONE
            )
            for row in csv_reader:
                word_nid = self.__webchild_nid(row["WordNet-synsetid"])
                word = row["#word"]
                # Skip edge generation if the word node already has a wn mapping,
                # or if the word is not represented in the yielded nodes,
                if (
                    word_nid not in yielded_words
                    or yielded_words[word_nid].lower() != word.lower()
                ):
                    continue
                lemma = "_".join(word.split())
                sense_num = row["sense-number"]
                synset_nid = f"wn:{lemma}.n.{int(sense_num):02d}"
                yield Edge(
                    datasource=self.__DATASOURCE_ID,
                    object_=synset_nid,
                    predicate=WN_SYNSET,
                    subject=word_nid,
                )
                # For tracking which nodes have mappings already
                # Deleting from yielded instead of tracking in a new set to save memory.
                del yielded_words[word_nid]

    def transform(
        self,
        *,
        memberof_csv_file_path: Path,
        physical_csv_file_path: Path,
        substanceof_csv_file_path: Path,
        wordnet_csv_file_path: Path,
    ) -> Generator[Union[Node, Edge], None, None]:
        yielded_words = {}
        part_whole_csv_files = (
            memberof_csv_file_path,
            physical_csv_file_path,
            substanceof_csv_file_path,
        )
        for csv_file_path in part_whole_csv_files:
            yield from self.__transform_webchild_file(
                csv_file_path=csv_file_path, yielded_words=yielded_words
            )
        yield from self.__transform_wordnet_csv(
            wordnet_csv_file_path=wordnet_csv_file_path, yielded_words=yielded_words
        )
        self._logger.info("Finished WebChild transform")
