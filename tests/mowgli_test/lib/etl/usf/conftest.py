import bz2
import pytest
from io import TextIOWrapper
from pathlib import Path
from tests.mowgli_test.lib.etl.http_client.mock_etl_http_client import MockEtlHttpClient


_sample_usf_file_path = Path(__file__).parent / 'usf_test_data.xml'



@pytest.fixture
def strengths():
    return open(_sample_usf_file_path)

@pytest.fixture
def url():
    return "https://mowgli.com/usf_test_data.zip"


@pytest.fixture
def usfclient():
    client = MockEtlHttpClient()
    
    def content_producer():
        return open("tests/mowgli_test/lib/etl/usf/usf_test_data.zip", 'rb')

    client.add_mock_response("https://mowgli.com/usf_test_data.zip",content_producer)
    return client