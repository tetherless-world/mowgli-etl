from typing import Optional, Tuple, Dict, Union

from mowgli.lib.cskg.node import Node


class Edge:
    def __init__(self, *, datasource: str, object_: Union[str, Node], relation: str, subject: Union[str, Node], other: Optional[Dict[str, object]]=None, weight: Optional[float]=None):
        self.__datasource = datasource
        self.__object = object_.id if isinstance(object_, Node) else object_
        self.__other = other
        self.__relation = relation
        self.__subject = subject.id if isinstance(subject, Node) else subject
        self.__weight = weight

    @property
    def datasource(self):
        return self.__datasource

    @property
    def id(self):
        return self.__id

    @property
    def object(self):
        return self.__object

    @property
    def relation(self):
        return self.__relation

    @property
    def other(self):
        return self.__other

    @property
    def weight(self):
        return self.__weight
