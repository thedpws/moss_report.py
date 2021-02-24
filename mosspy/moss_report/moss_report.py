from abc import ABC, abstractmethod
import os
import re
from html.parser import HTMLParser



class MossSimilarity(ABC):
    """Representation of the similarity between two programs, referred to as "self" and "other"."""

    @property
    @abstractmethod
    def self_code(self) -> str:
        """Returns self's code"""

    @property
    @abstractmethod
    def self_filename(self) -> str:
        """Returns self's filename"""

    @property
    @abstractmethod
    def self_code_block_slices(self) -> List[Tuple[int, int]]:
        """Returns the start-end indices of the code blocks of "self" found to be similar to other"""

    @property
    @abstractmethod
    def self_percent_similar(self) -> float:
        """Returns the percent of self's code that is found to be similar to other's"""

    @property
    @abstractmethod
    def other_code(self) -> str:
        """Returns other's code"""

    @property
    @abstractmethod
    def other_filename(self) -> str:
        """Returns other's filename"""

    @property
    @abstractmethod
    def other_code_block_slices(self) -> List[Tuple[int, int]]:
        """Returns the start-end indices of the code blocks of "other" found to be similar to self"""

    @property
    @abstractmethod
    def other_percent_similar(self) -> float:
        """Returns the percent of other's code that is found to be similar to self's"""

    def __getattr__(self, name) -> Any:
        """Gets meta attributes attached in pre-parsing."""
        # TODO: Give warning when attaching metadata with name in [code, filename, code_block_slices]
        if name.startswith('self_'):
            return getattr(self._self, name.removeprefix('self_'))
        elif name.startswith('other_'):
            return getattr(self._other, name.removeprefix('other_'))
        else:
            raise AttributeError(f'Attribute {name} not found')

    @property
    @abstractmethod
    def self(self):
        """Returns the metadata of self"""

    @property
    @abstractmethod
    def other(other):
        """Returns the metadata of other"""


class MossReport(ABC):

    @property
    def get_similarities(self, self_filename: str) -> List[MossSimilarity]:
        """Returns the similarities of the program with filename "self_filename"."""

