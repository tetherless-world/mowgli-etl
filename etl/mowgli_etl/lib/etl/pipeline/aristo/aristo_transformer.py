import csv
from collections import Counter
from pathlib import Path
from urllib.parse import quote

from mowgli_etl.lib.cskg.concept_net_predicates import IS_A, HAS_A, PART_OF, LOCATED_NEAR, HAS_FIRST_SUBEVENT, CAUSES, \
    CREATED_BY, HAS_PREREQUISITE, AT_LOCATION
from mowgli_etl.lib.cskg.edge import Edge
from mowgli_etl.lib.cskg.node import Node
from mowgli_etl.lib.etl._transformer import _Transformer
from mowgli_etl.lib.etl.word_net_id import WordNetId


class AristoTransformer(_Transformer):
    __DATASOURCE = "aristo"

    class __PredToConceptNetPredicateMapping:
        def __init__(self, concept_net_predicate: str, reverse_args: bool = False):
            self.concept_net_predicate = concept_net_predicate
            self.reverse_args = reverse_args

    __PRED_TO_CONCEPT_NET_PREDICATE_MAPPINGS = {
        "be behind": __PredToConceptNetPredicateMapping(LOCATED_NEAR),
        "cause": __PredToConceptNetPredicateMapping(CAUSES),
        "cause by": __PredToConceptNetPredicateMapping(CAUSES, reverse_args=True),
        "consist of": __PredToConceptNetPredicateMapping(HAS_A),
        "contain": __PredToConceptNetPredicateMapping(HAS_A),
        "create": __PredToConceptNetPredicateMapping(CREATED_BY, reverse_args=True),
        "depend on": __PredToConceptNetPredicateMapping(HAS_PREREQUISITE),
        "has-part": __PredToConceptNetPredicateMapping(HAS_A),
        "have": __PredToConceptNetPredicateMapping(HAS_A),
        "include": __PredToConceptNetPredicateMapping(HAS_A),
        "isa": __PredToConceptNetPredicateMapping(IS_A),
        "is-part-of": __PredToConceptNetPredicateMapping(PART_OF),
        "live in": __PredToConceptNetPredicateMapping(AT_LOCATION),
        # "occur in": __PredToConceptNetPredicateMapping(AT_LOCATION),
        "possess": __PredToConceptNetPredicateMapping(HAS_A),
        "produce": __PredToConceptNetPredicateMapping(CREATED_BY, reverse_args=True),
        "require": __PredToConceptNetPredicateMapping(HAS_PREREQUISITE),
        "start with": __PredToConceptNetPredicateMapping(HAS_FIRST_SUBEVENT),
        "within": __PredToConceptNetPredicateMapping(PART_OF)
    }

    def __create_type_edge(self, *, arg_node: Node, type_word_net_id: WordNetId) -> Edge:
        # arg node IsA WordNet node
        # Only yield this once, when the arg is yielded.
        return \
            Edge(
                datasource=self.__DATASOURCE,
                object="wn:" + str(type_word_net_id),
                predicate=IS_A,
                subject=arg_node.id,
            )

    def __parse_arg(self, *, arg: str, provenance: str, type_: str) -> Node:
        # Put the type in the id in case words are reused
        if type_ != "Thing":
            word_net_type = type_.rsplit('_', 1)
            assert len(word_net_type[1]) >= 2
            type_word_net_id = WordNetId(word=word_net_type[0], pos=word_net_type[1][0],
                                         offset=int(word_net_type[1][1:]))
        else:
            type_word_net_id = None

        node = \
            Node(
                datasource=self.__DATASOURCE,
                id=f"{self.__DATASOURCE}:{type_}:{quote(arg)}",
                label=arg,
                # Assume the part of speech of the arg is the same as the part of speech of the type
                pos=type_word_net_id.pos if type_word_net_id is not None else None,
                other={"provenance": provenance, "type": type_}
            )
        return node, type_word_net_id

    # @staticmethod
    # def __to_bool(value: str) -> bool:
    #     value = value.strip()
    #     if value == "y":
    #         return True
    #     elif value == "n":
    #         return False
    #     else:
    #         return None

    def transform(self, combined_kb_tsv_file_path: Path):
        yielded_edges_tree = {}
        yielded_node_ids = set()
        unmapped_preds = Counter()
        with open(combined_kb_tsv_file_path, "r") as combined_kb_tsv_file:
            for row in csv.DictReader(combined_kb_tsv_file, delimiter='\t'):
                # QStrength	- The quantification strength of the triple (0-1), where 1 = applies to most members of Arg1, 0 = applies to just a few members of Arg1.
                # The scale is purely a ranking scale (has no probabilistic meaning) - feel free to rescale it as required for your application.
                # Quantifier	- Simple qualitative quantifier: if QStrength > 0.5 it is "most", otherwise it is "some".
                # Arg1		- in (Arg1 Pred Arg2)
                # Pred		- in (Arg1 Pred Arg2)
                # Arg2		- in (Arg1 Pred Arg2)
                # Sentence	- Expression of this tuple as an English sentence.
                # Score	- This score is now redundant (superceded by QStrength), but was the either Turk-derived or model-derived quality of the tuple (range 0-1)
                # Inferred?	- "n": The tuple was directly extracted from text, WordNet, or produced by KBCompletion. The source sentence(s) id(s) are listed in the Provenance field.
                # "y": The tuple was inferred using schema mapping rule(s) from other tuple(s). The source tuple(s) are listed in the Provenance field.
                # "m": Mixed - the tuple was both extracted from text and inferred. The source sentences and tuples are listed in the Provenance field.
                # Multiword?	- If the Arg1 or Arg2 include a multiword, this is "y", else "n"
                # Canonical?	- The tuple is in its canonical (normalized) form. (We retain both the original and canonical forms in this database).
                # Non-canonical tuples are also transformed to a canonical form, elsewhere in the database.
                # Domain	- The general type of Arg1
                # Range	- The general type of Arg2
                # Provenance	- KBCompletion - inferred by KB Completion methods.
                # WordNet3.0 - tuple comes from WordNet v3.0.
                # ("cat","eat","food") - tuple was inferred from this tuple using a schema mapping rule (see TACL paper)
                # 12413 - tuple was extracted from sentence 12413. Source setnences are available on request.

                # Pull the columns out into typed variables
                qstrength = float(row["QStrength"])
                quantifier = row["Quantifier"].strip()
                assert quantifier
                arg1 = row["Arg1"].strip()
                assert arg1
                pred = row["Pred"].strip()
                assert pred
                arg2 = row["Arg2"].strip()
                assert arg2
                # we selected 49 types (with help from WordNet) to mark the domain/range of triples (see below), plus "Thing" for the remainder.
                domain = row["Domain"].strip()
                assert domain
                range = row["Range"].strip()
                assert range
                provenance = row["Provenance"].strip()
                assert provenance

                # Mapping multiple preds to a single edge type may lead to duplicate edges
                concept_net_predicate_mapping = self.__PRED_TO_CONCEPT_NET_PREDICATE_MAPPINGS.get(pred)
                if concept_net_predicate_mapping is None:
                    if pred not in unmapped_preds:
                        self._logger.debug("ignoring unmapped pred %s: %s %s %s", pred, arg1, pred, arg2)
                    unmapped_preds[pred] += 1
                    continue

                concept_net_predicate = concept_net_predicate_mapping.concept_net_predicate
                reverse_args = concept_net_predicate_mapping.reverse_args

                # Convert arg1 and arg2 into nodes
                subject_node, subject_type_word_net_id = self.__parse_arg(arg=arg1, provenance=provenance, type_=domain)
                object_node, object_type_word_net_id = self.__parse_arg(arg=arg2, provenance=provenance, type_=range)

                for arg_node, type_word_net_id in (
                        (subject_node, subject_type_word_net_id),
                        (object_node, object_type_word_net_id)
                ):
                    if arg_node.id in yielded_node_ids:
                        continue
                    # arg_node has not been yielded yet

                    yield arg_node
                    yielded_node_ids.add(arg_node.id)

                    # The domain or range (type) is a WordNet synset, or "Thing" if unknown
                    # Only yield this edge once, along with the node.
                    if type_word_net_id is not None:
                        yield self.__create_type_edge(arg_node=arg_node, type_word_net_id=type_word_net_id)

                # Yield the tuple as an Edge if an equivalent edge hasn't been yielded before
                if reverse_args:
                    # The pred -> predicate mapping above told us that the object should be the subject and the subject the object
                    # ConceptNet has few symmetric relations. For example, it has "CreatedBy" but not "Creates".
                    # So we map "produce" to "CreatedBy" and reverse the args.
                    subject_node, object_node = object_node, subject_node
                object_edges = yielded_edges_tree.setdefault(subject_node.id, {}).setdefault(object_node.id, set())
                if concept_net_predicate in object_edges:
                    continue

                yield \
                    Edge(
                        datasource=self.__DATASOURCE,
                        predicate=concept_net_predicate,
                        subject=subject_node.id,
                        object=object_node.id,
                        weight=qstrength,
                    )
                object_edges.add(concept_net_predicate)

            self._logger.info("top unmapped preds: %s", unmapped_preds.most_common(20))
