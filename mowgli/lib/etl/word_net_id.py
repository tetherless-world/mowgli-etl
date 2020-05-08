from typing import NamedTuple


class WordNetId(NamedTuple):
    word: str
    pos: str
    offset: int

    @classmethod
    def parse(cls, value: str):
        value_split = value.split(".")
        assert len(value_split) == 3, value
        word, pos, offset = value_split
        assert len(pos) == 1, value
        offset = int(offset)
        return cls(word=word, pos=pos, offset=offset)

    def __str__(self):
        return f"{self.word}.{self.pos}.{self.offset:02d}"
