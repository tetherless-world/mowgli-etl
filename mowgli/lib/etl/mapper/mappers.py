from mowgli.lib._closeable import _Closeable


class Mappers:
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

        try:
            concept_net_index = ConceptNetIndex.open()
        except FileNotFoundError:
            concept_net_index = ConceptNetIndex.create()
        return ConceptNetMapper(concept_net_index)
