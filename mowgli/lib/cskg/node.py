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

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented
    
    def __hash__(self):
        return hash((
            self.__aliases,
            self.__datasource,
            self.__id,
            self.__label,
            self.__other,
            self.__pos
        ))

    @property
    def id(self):
        return self.__id

    @property
    def label(self):
        return self.__label

    @property
    def other(self):
        return self.__other

    @property
    def pos(self):
        return self.__pos

    def __repr__(self):
        key_vals = ', '.join(f'{key}={val}' for key, val in sorted(self.__dict__.items()))
        return f'{self.__class__.__name__}({key_vals})'
