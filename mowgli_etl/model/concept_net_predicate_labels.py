from mowgli_etl.model import concept_net_predicates as __concept_net_predicates

CONCEPT_NET_PREDICATE_LABELS = {
    __concept_net_predicates.ANTONYM: "is an antonym of",
    __concept_net_predicates.AT_LOCATION: "is at location",
    __concept_net_predicates.CAPABLE_OF: "is capable of",
    __concept_net_predicates.CAUSES: "causes",
    __concept_net_predicates.CAUSES_DESIRE: "causes desire of",
    __concept_net_predicates.CREATED_BY: "is created by",
    __concept_net_predicates.DEFINED_AS: "is defined as",
    __concept_net_predicates.DERIVED_FROM: "is derived from",
    __concept_net_predicates.DESIRES: "desires",
    __concept_net_predicates.DISTINCT_FROM: "is distinct from",
    __concept_net_predicates.ETYMOLOGICALLY_DERIVED_FROM: "is etymologically derived from",
    __concept_net_predicates.ETYMOLOGICALLY_RELATED_TO: "is etymologically related to",
    __concept_net_predicates.EXTERNAL_URL: "has external URL",
    __concept_net_predicates.FORM_OF: "is a form of",
    __concept_net_predicates.HAS_A: "has a",
    __concept_net_predicates.HAS_CONTEXT: "has context",
    __concept_net_predicates.HAS_SUBEVENT: "has subevent",
    __concept_net_predicates.HAS_FIRST_SUBEVENT: "has first subevent",
    __concept_net_predicates.HAS_LAST_SUBEVENT: "has last subevent",
    __concept_net_predicates.HAS_PROPERTY: "has property",
    __concept_net_predicates.HAS_PREREQUISITE: "has prerequisite",
    __concept_net_predicates.IS_A: "is a type of",
    __concept_net_predicates.LOCATED_NEAR: "is located near",
    __concept_net_predicates.MADE_OF: "is made of",
    __concept_net_predicates.MANNER_OF: "is a manner of",
    __concept_net_predicates.MOTIVATED_BY_GOAL: "is motivated by the goal",
    __concept_net_predicates.OBSTRUCTED_BY: "is obstructed by",
    __concept_net_predicates.PART_OF: "is part of",
    __concept_net_predicates.RECEIVES_ACTION: "receives action",
    __concept_net_predicates.RELATED_TO: "is related to",
    __concept_net_predicates.SIMILAR_TO: "is similar to",
    __concept_net_predicates.SYMBOL_OF: "is a symbol of",
    __concept_net_predicates.SYNONYM: "is a synonym of",
    __concept_net_predicates.USED_FOR: "is used for",
}

for __attr in dir(__concept_net_predicates):
    if __attr.startswith("_"):
        continue
    __predicate = getattr(__concept_net_predicates, __attr)
    assert __predicate in CONCEPT_NET_PREDICATE_LABELS, __predicate
