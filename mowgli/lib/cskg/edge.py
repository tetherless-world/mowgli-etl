import json
from typing import Optional, Dict, Union

from mowgli.lib.cskg.node import Node


class Edge:
    def __init__(self, *, datasource: str, object_: Union[str, Node], predicate: str, subject: Union[str, Node],
                 other: Optional[Dict[str, object]] = None, weight: Optional[float] = None):
        self.__datasource = datasource
        self.__object = object_.id if isinstance(object_, Node) else object_
        self.__other = other
        self.__predicate = predicate
        self.__subject = subject.id if isinstance(subject, Node) else subject
        self.__weight = weight

    @property
    def datasource(self):
        return self.__datasource

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        if self.__datasource != other.__datasource:
            return False
        if self.__object != other.__object:
            return False
        if self.__other != other.__other:
            return False
        if self.__predicate != other.__predicate:
            return False
        if self.__subject != other.__subject:
            return False
        if self.__weight != other.__weight:
            return False
        return True

    def __hash__(self):
        return hash((
            self.__datasource,
            self.__object,
            json.dumps(self.__other, sort_keys=True),
            self.__predicate,
            self.__subject,
            self.__weight
        ))

    @property
    def object(self):
        return self.__object

    @property
    def other(self):
        return self.__other

    @property
    def predicate(self):
        return self.__predicate

    @property
    def subject(self):
        return self.__subject

    def __repr__(self):
        key_vals = ', '.join(f'{key}={val}' for key, val in sorted(self.__dict__.items()))
        return f'{self.__class__.__name__}({key_vals})'

    @property
    def weight(self):
        return self.__weight
