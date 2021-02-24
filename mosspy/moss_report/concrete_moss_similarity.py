from typing import List, Tuple
from .moss_report import MossSimilarity

class ConcreteMossSimilarity(MossSimilarity):

    _EXPECTED_ATTRS = ['code', 'filename', 'code_block_slices', 'percent_similar']

    def __init__(_self, self, other):
        self_missing_attrs = [attr for attr in _self._EXPECTED_ATTRS if not hasattr(self, attr)]
        other_missing_attrs = [attr for attr in _self._EXPECTED_ATTRS if not hasattr(other, attr)]

        if self_missing_attrs or other_missing_attrs:
            raise AttributeError(' and '.join([f'expected "self" to have attributes {self_missing_attrs}', f'expected "other" to have attributes {other_missing_attrs}']).capitalize())

        _self._self = self
        _self._other = other

    @property
    def self_code(self) -> str:
        return self._self.code

    @property
    def self_filename(self) -> str:
        return self._self.filename

    @property
    def self_code_block_slices(self) -> List[Tuple[int, int]]:
        return self._self.code_block_slices

    @property
    def self_percent_similar(self) -> float:
        return self._self.percent_similar

    @property
    def other_code(self) -> str:
        return self._other.code

    @property
    def other_filename(self) -> str:
        return self._other.filename

    @property
    def other_code_block_slices(self) -> List[Tuple[int, int]]:
        return self._other.code_block_slices

    @property
    def other_percent_similar(self) -> float:
        return self._other.percent_similar

    @property
    def self(self):
        return self.other

    @property
    def other(self):
        return self.other

