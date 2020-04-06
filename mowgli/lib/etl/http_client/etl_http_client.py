from abc import ABC, abstractmethod
from typing import IO


class EtlHttpClient(ABC):
    @abstractmethod
    def urlopen(self, url: str) -> IO:
        raise NotImplementedError()
