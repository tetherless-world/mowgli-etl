from typing import Optional, Tuple, Dict


class Node:
    def __init__(self, *, datasource: str, id: str, label: str, aliases: Optional[Tuple[str, ...]] = None, other: Optional[Dict[str, object]] = None, pos: Optional[str] = None):
        self.__aliases = aliases
        self.__datasource = datasource
        self.__id = id
        self.__label = label
        self.__other = other
        self.__pos = pos

    @property
    def aliases(self):
        return self.__aliases

    @property
    def datasource(self):
        return self.__datasource

    @property
    def id(self):
        return self.__id

    @property
    def label(self):
        return self.__label

    @property
    def other(self):
        return self.__other

    def pos(self):
        return self.__pos
