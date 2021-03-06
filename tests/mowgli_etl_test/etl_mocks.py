from typing import Optional, Dict, List, Generator, Union, Iterable

from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.model.kg_node import KgNode
from mowgli_etl._extractor import _Extractor
from mowgli_etl._pipeline import _Pipeline
from mowgli_etl._transformer import _Transformer


class MockExtractor(_Extractor):
    def __init__(self, extraction_kwargs: Dict[str, object] = None):
        self.__extraction_kwargs = extraction_kwargs

    def extract(self, **kwargs) -> Optional[Dict[str, object]]:
        return self.__extraction_kwargs if self.__extraction_kwargs is not None else {}


class MockTransformer(_Transformer):
    def __init__(self, graph_iterator: Iterable[Union[KgNode, KgEdge]] = tuple()):
        self.__graph_iterator = graph_iterator

    def transform(self, **kwds) -> Generator[Union[KgNode, KgEdge], None, None]:
        yield from self.__graph_iterator


class MockPipeline(_Pipeline):
    def __init__(self, *, id: str = 'test', extractor: Optional[_Extractor] = None,
                 transformer: Optional[_Transformer] = None, **kwargs):
        super().__init__(
            id=id,
            extractor=extractor if extractor is not None else MockExtractor(),
            transformer=transformer if transformer is not None else MockTransformer(),
            **kwargs
        )
