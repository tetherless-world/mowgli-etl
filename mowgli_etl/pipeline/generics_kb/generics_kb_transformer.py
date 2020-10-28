import csv
from pathlib import Path
from urllib.parse import quote_plus

from mowgli_etl._transformer import _Transformer
from mowgli_etl.model import concept_net_predicates
from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.model.kg_node import KgNode
from mowgli_etl.storage.mem_id_set import MemIdSet


class GenericsKbTransformer(_Transformer):
    # Ignore sources that are already incorporated into the CSKG.
    __IGNORE_SOURCES = {"ConceptNet", "TupleKB"}

    @property
    def __source_id(self):
        # Avoid circular dependency
        from mowgli_etl.pipeline.generics_kb.generics_kb_pipeline import (
            GenericsKbPipeline,
        )

        return GenericsKbPipeline.ID

    def transform(self, tsv_file_path: Path):
        yielded_edge_ids = MemIdSet()
        yielded_node_ids = MemIdSet()

        with open(tsv_file_path) as tsv_file:
            for row in csv.DictReader(tsv_file, delimiter="\t"):
                source = row["SOURCE"].strip()
                term = row["TERM"].strip()
                quantifier = row["QUANTIFIER"].strip()
                generic_sentence = row["GENERIC SENTENCE"].strip()
                score = row["SCORE"].strip()

                if source in self.__IGNORE_SOURCES:
                    continue

                assert generic_sentence
                assert term

                # term is the subject
                subject_node = KgNode(
                    id=f"{self.__source_id}:{quote_plus(term)}",
                    labels=(term,),
                    source_ids=(self.__source_id,),
                )

                # TODO: do more sophisticated processing of the generic sentence to get
                # (1) a verb? that is mapped to one of the ConceptNet predicates
                # (2) the object node
                # The subject should always be the term (?)
                generic_sentence_lower = generic_sentence.lower()
                generic_sentence_split = generic_sentence_lower.split()
                if (
                    generic_sentence_split[0] == term
                    and generic_sentence_split[1] == "isa"
                    and len(generic_sentence_split) > 2
                ):
                    # Sentences of the form "Aardvark isa mammal."
                    object_label = " ".join(generic_sentence_split[2:]).rstrip(".")
                    object_node = KgNode(
                        id=f"{self.__source_id}:{quote_plus(object_label)}",
                        labels=(object_label,),
                        source_ids=(self.__source_id,),
                    )
                    predicate = concept_net_predicates.IS_A
                    # Yields triples such as (generics_kb:snowfall, /r/IsA, generics_kb:precipitation)
                else:
                    continue

                for node in (subject_node, object_node):
                    if node.id not in yielded_node_ids:
                        # Only yield a unique node (per id) once
                        yield node
                        yielded_node_ids.add(node.id)

                edge = KgEdge.with_generated_id(
                    object=object_node.id,
                    predicate=predicate,
                    source_ids=(self.__source_id,),
                    subject=subject_node.id,
                )
                if edge.id not in yielded_edge_ids:
                    # Don't yield duplicate edges. The edge id is generated from the (subject, predicate, object) triple.
                    yield edge
                    self._logger.info(
                        "(%s, %s, %s)", edge.subject, edge.predicate, edge.object
                    )
                    yielded_edge_ids.add(edge.id)
