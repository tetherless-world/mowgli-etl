from typing import Generator, Union

from xml.dom.minidom import parse

from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.model.kg_node import KgNode
from mowgli_etl._transformer import _Transformer
from mowgli_etl.pipeline.sentic import sentic_types
from mowgli_etl.pipeline.sentic.sentic_constants import SENTIC_FILE_KEY
from mowgli_etl.pipeline.sentic.sentic_mappers import (
    sentic_edge,
    sentic_id,
    sentic_node,
)


class SENTICTransformer(_Transformer):
    def transform(self, **kwds) -> Generator[Union[KgNode, KgEdge], None, None]:

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
                subj_sentic_id = named_ind_ele.getAttribute("rdf:about").split("#")[-1]

                type_ele = named_ind_ele.getElementsByTagName("rdf:type")[0]
                subj_type = type_ele.getAttribute("rdf:resource").split("#")[-1]

                if subj_type != sentic_types.CONCEPT:
                    continue

                label = named_ind_ele.getElementsByTagName("text")[
                    0
                ].firstChild.nodeValue

                subject_node = sentic_node(
                    id=subj_sentic_id, label=label, sentic_type=sentic_types.CONCEPT
                )
                yield subject_node

                # Dataset contains duplicate semantic relation designations
                yielded_related_nids = set()
                for semantic_ele in named_ind_ele.getElementsByTagName("semantics"):
                    related_nid = sentic_id(
                        semantic_ele.getAttribute("rdf:resource").split("#")[-1],
                        sentic_types.CONCEPT,
                    )
                    if related_nid not in yielded_related_nids:
                        yield sentic_edge(subject=subject_node.id, object_=related_nid)
                        yielded_related_nids.add(related_nid)

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

                # Dataset contains duplicate primitive assignments
                yielded_primitives = set()
                for primitive_ele in named_ind_ele.getElementsByTagName("primitiveURI"):
                    primitive = primitive_ele.getAttribute("rdf:resource").split("#")[
                        -1
                    ]
                    if primitive not in yielded_primitives:
                        primitive_node = sentic_node(
                            id=primitive, sentic_type=sentic_types.PRIMITIVE
                        )
                        yield primitive_node
                        yield sentic_edge(
                            subject=subject_node.id, object_=primitive_node.id,
                        )
                        yielded_primitives.add(primitive)
