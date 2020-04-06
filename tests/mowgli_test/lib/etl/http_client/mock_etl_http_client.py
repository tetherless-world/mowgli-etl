from io import StringIO
from typing import IO, Callable, Union

from mowgli.lib.etl.http_client.etl_http_client import EtlHttpClient


class MockEtlHttpClient(EtlHttpClient):
    def __init__(self):
        self.__mock_responses = {}

    def urlopen(self, url: str) -> IO:
        assert url in self.__mock_responses, "Unexpected url %s" % url
        return self.__mock_responses[url]()

    def __constant_mock_response(self, text: str) -> Callable[[], StringIO]:
        def mock_response():
            return StringIO(text)

        return mock_response

    def add_mock_response(self, url: str, response: Union[str, Callable[[], IO]]):
        response_producer = response
        if not isinstance(response, Callable):
            assert isinstance(response, str)
            response_producer = self.__constant_mock_response(response)
        self.__mock_responses[url] = response_producer
        return self
