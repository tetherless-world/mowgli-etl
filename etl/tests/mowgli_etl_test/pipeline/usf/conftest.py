import bz2
import pytest
from io import TextIOWrapper
from pathlib import Path
from tests.mowgli_etl_test.http_client.mock_etl_http_client import MockEtlHttpClient


_sample_usf_file_path = Path(__file__).parent / "usf_test_data.xml"

_sample_usf_zip_file_path = Path(__file__).parent / "usf_test_data.zip"


@pytest.fixture
def strengths():
    return open(_sample_usf_file_path)


@pytest.fixture
def url():
    return "https://mowgli.com/usf_test_data.zip"


@pytest.fixture
def usfclient(url):
    client = MockEtlHttpClient()
    client.add_file_mock_response(url, _sample_usf_zip_file_path)
    return client
