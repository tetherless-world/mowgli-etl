from pathlib import Path
from typing import Optional, Tuple

from rdflib import Graph, RDF, OWL, RDFS, URIRef

from mowgli.lib.cskg import concept_net_predicates
from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl._transformer import _Transformer


class FoodOnTransformer(_Transformer):
    _DATASOURCE = "foodon"

    class __FoodOnClass:
        _URI_PREFIX = "http://purl.obolibrary.org/obo/FOODON_"

        def __init__(self, *, label: str, sub_class_of: Optional[Tuple[URIRef, ...]], uri: URIRef):
            self.label = label
            self.sub_class_of = sub_class_of
            self.uri = uri

            self.node = \
                Node(
                    datasource=FoodOnTransformer._DATASOURCE,
                    id="foodon:" + str(uri)[len(self._URI_PREFIX):],
                    label=label
                )
            self.node_yielded = False

    def transform(self, food_on_owl_file_path: Path):
        graph = Graph()
        self._logger.info("parsing FoodOn OWL")
        graph.parse(source=str(food_on_owl_file_path))
        self._logger.info("parsed FoodOn OWL")

        self._logger.info("parsing FoodOn classes")

        classes_by_uri = {}
        for class_uri in graph.subjects(RDF.type, OWL.Class):
            if not str(class_uri).startswith(self.__FoodOnClass._URI_PREFIX):
                continue
            labels = tuple(graph.objects(class_uri, RDFS.label))
            if not labels:
                continue
            # Just use the first label
            label = labels[0]
            assert label, class_uri

            sub_class_of = tuple(graph.objects(class_uri, RDFS.subClassOf))
            if not sub_class_of:
                continue

            class_ = self.__FoodOnClass(
                label=label,
                sub_class_of=sub_class_of,
                uri=class_uri
            )
            assert class_.uri not in classes_by_uri
            classes_by_uri[class_.uri] = class_
        self._logger.info("parsed %d classes from FoodOn", len(classes_by_uri))

        for class_ in classes_by_uri.values():
            for sub_class_of in class_.sub_class_of:
                parent_class = classes_by_uri.get(sub_class_of)
                if not parent_class:
                    continue
                # Only yield nodes that are part of an edge.
                if not class_.node_yielded:
                    yield class_.node
                    class_.node_yielded = True
                if not parent_class.node_yielded:
                    yield parent_class.node
                    parent_class.node_yielded = True
                edge = \
                    Edge(
                        datasource=self._DATASOURCE,
                        subject=class_.node,
                        predicate=concept_net_predicates.IS_A,
                        object_=parent_class.node
                    )
                yield edge
