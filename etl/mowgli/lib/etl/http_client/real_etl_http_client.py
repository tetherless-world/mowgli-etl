from typing import IO
from urllib.request import urlopen

from mowgli.lib.etl.http_client.etl_http_client import EtlHttpClient


class RealEtlHttpClient(EtlHttpClient):
    def urlopen(self, url: str) -> IO:
        return urlopen(url)
