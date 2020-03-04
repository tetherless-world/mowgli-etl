from typing import Optional, Dict, List, Generator, Union

from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl._extractor import _Extractor
from mowgli.lib.etl._pipeline import _Pipeline
from mowgli.lib.etl._transformer import _Transformer


class MockExtractor(_Extractor):
    def __init__(self, extraction_kwargs: Dict[str, object] = None):
        self.__extraction_kwargs = extraction_kwargs

    def extract(self, **kwargs) -> Optional[Dict[str, object]]:
        return self.__extraction_kwargs if self.__extraction_kwargs is not None else {}


class MockTransformer(_Transformer):
    def __init__(self, nodes: List[Node] = None, edges: List[Edge] = None):
        self.__nodes = nodes
        self.__edges = edges

    def transform(self, **kwds) -> Generator[Union[Node, Edge], None, None]:
        if self.__nodes is not None:
            yield from self.__nodes
        if self.__edges is not None:
            yield from self.__edges


class MockPipeline(_Pipeline):
    def __init__(self, *, id: str = 'test', extractor: Optional[_Extractor] = None,
                 transformer: Optional[_Transformer] = None, **kwargs):
        super().__init__(
            id=id,
            extractor=extractor if extractor is not None else MockExtractor(),
            transformer=transformer if transformer is not None else MockTransformer()
        )
