from io import StringIO
from pathlib import Path
from typing import IO, Callable, Union

from mowgli_etl.lib.etl.http_client.etl_http_client import EtlHttpClient


class MockEtlHttpClient(EtlHttpClient):
    def __init__(self):
        self.__mock_responses = {}

    def urlopen(self, url: str) -> IO:
        assert url in self.__mock_responses, "Unexpected url %s" % url
        return self.__mock_responses[url]()

    def add_callable_mock_response(self, url: str, response_producer: Callable[[], IO]):
        self.__mock_responses[url] = response_producer
        return self

    def add_text_mock_response(self, url: str, text: str):
        def produce_response():
            return StringIO(text)
        return self.add_callable_mock_response(url, produce_response)

    def add_file_mock_response(self, url: str, file_path: Path):
        def produce_response():
            return open(file_path, 'rb')
        return self.add_callable_mock_response(url, produce_response)
