from typing import Generator, Union

from xml.dom.minidom import parse

from mowgli_etl.model.edge import Edge
from mowgli_etl.model.node import Node
from mowgli_etl._transformer import _Transformer
from mowgli_etl.pipeline.sentic import sentic_types
from mowgli_etl.pipeline.sentic.sentic_constants import SENTIC_FILE_KEY
from mowgli_etl.pipeline.sentic.sentic_mappers import (
    sentic_edge,
    sentic_id,
    sentic_node,
)


class SENTICTransformer(_Transformer):
    def transform(self, **kwds) -> Generator[Union[Node, Edge], None, None]:

        self._logger.info("transform %s", SENTIC_FILE_KEY)

        with open(kwds[SENTIC_FILE_KEY], mode="r") as sentic_file:
            dom = parse(sentic_file)

            sentic_fields = (
                "pleasantness",
                "attention",
                "sensitivity",
                "aptitude",
                "polarity",
            )

            for named_ind_ele in dom.getElementsByTagName("owl:NamedIndividual"):
                id = named_ind_ele.getAttribute("rdf:about").split("#")[-1]

                type_ele = named_ind_ele.getElementsByTagName("rdf:type")[0]
                type = type_ele.getAttribute("rdf:resource").split("#")[-1]

                if type != sentic_types.CONCEPT:
                    continue

                label = named_ind_ele.getElementsByTagName("text")[
                    0
                ].firstChild.nodeValue

                subject_node = sentic_node(
                    id=id, label=label, sentic_type=sentic_types.CONCEPT
                )
                yield subject_node

                for semantic_ele in named_ind_ele.getElementsByTagName("semantics"):
                    related_nid = sentic_id(
                        semantic_ele.getAttribute("rdf:resource").split("#")[-1]
                    )
                    yield sentic_edge(subject=subject_node.id, object_=related_nid)

                for sentic_name in sentic_fields:
                    sentic_eles = named_ind_ele.getElementsByTagName(sentic_name)
                    if len(sentic_eles) == 0:
                        continue

                    raw_weight = (
                        named_ind_ele.getElementsByTagName(sentic_name)[0]
                        .childNodes[0]
                        .data
                    )

                    weight = float(raw_weight)
                    object_node = sentic_node(
                        id=sentic_name, sentic_type=sentic_types.SENTIC
                    )
                    yield object_node
                    yield sentic_edge(
                        subject=subject_node.id, object_=object_node.id, weight=weight,
                    )

                for primitive_ele in named_ind_ele.getElementsByTagName("primitiveURI"):
                    primitive = primitive_ele.getAttribute("rdf:resource").split("#")[
                        -1
                    ]
                    primitive_node = sentic_node(
                        id=primitive, sentic_type=sentic_types.PRIMITIVE
                    )
                    yield primitive_node
                    yield sentic_edge(
                        subject=subject_node.id, object_=primitive_node.id,
                    )
