from pathlib import Path
from typing import Optional

from mowgli.lib._closeable import _Closeable


class Mappers:
    def __init__(self, *, concept_net_index_directory_path: Optional[Path] = None):
        self.__concept_net_index_directory_path = concept_net_index_directory_path

    def __enter__(self):
        mappers = []
        mappers.append(self.__new_concept_net_mapper())
        self.__mappers = tuple(mapper for mapper in mappers if mapper is not None)
        return self.__mappers

    def __exit__(self, *args, **kwds):
        for mapper in self.__mappers:
            if isinstance(mapper, _Closeable):
                mapper.close()
        self.__mappers = None

    def __new_concept_net_mapper(self):
        try:
            from mowgli.lib.etl.mapper.concept_net.concept_net_index import ConceptNetIndex
            from mowgli.lib.etl.mapper.concept_net.concept_net_mapper import ConceptNetMapper
        except ImportError:
            return None

        concept_net_index_kwds = {}
        if self.__concept_net_index_directory_path is not None:
            concept_net_index_kwds["directory_path"] = self.__concept_net_index_directory_path

        try:
            concept_net_index = ConceptNetIndex.open(**concept_net_index_kwds)
        except FileNotFoundError:
            concept_net_index = ConceptNetIndex.create(**concept_net_index_kwds)
        return ConceptNetMapper(concept_net_index)
