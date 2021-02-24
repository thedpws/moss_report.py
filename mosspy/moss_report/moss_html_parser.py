import os
import re
from html.parser import HTMLParser

import requests

from main.plagiarisms.filename import parse_big_filename


class MossFrameParser(HTMLParser):
    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):

        if not hasattr(self, '_codes'):
            self._codes = list()

        if tag == 'font':
            self._capture_data = True

    def handle_endtag(self, tag):
        if tag == 'font':
            self._capture_data = False

    def handle_data(self, data):
        if not hasattr(self, '_capture_data'):
            self._capture_data = False

        if self._capture_data and data:
            self._codes.append(data)


class MossMatchParser(HTMLParser):
    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):

        if not hasattr(self, '_codes'):
            self._codes = list()

        if tag == 'frame':
            url = self._base_url + '/' + dict(attrs)['src']
            frame = requests.get(url).content.decode(errors='ignore')
            frame_parser = MossFrameParser()
            frame_parser.feed(frame)
            if frame_parser._codes:
                self._codes.append(''.join(frame_parser._codes))


class MossHTMLParser(HTMLParser):

    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        if not hasattr(self, '_code_similarities'):
            self._code_similarities = dict()

        self._capture_data = tag == 'a' and [(attr, val) for (attr, val) in attrs if
                                             attr == 'href' and val.startswith('http://moss.stanford.edu/results')]

        if self._capture_data:
            self._url = [(attr, val) for (attr, val) in attrs if attr == 'href'][0][1]

            if self._url not in self._code_similarities:
                self._code_similarities[self._url] = list()

    def _parse_data(self, data):

        filepath = re.sub(r' \(\d+%\)', '', data)
        percent_similar = float('0.' + re.search(r'\((\d+)%\)', data).group(1))
        big_filename = os.path.basename(filepath)

        student_id, filename = parse_big_filename(big_filename)

        # TODO: implement :)
        code_block_slices: List[Tuple[int, int]] = []

        return student_id, filename, percent_similar, code_block_slices

    def handle_data(self, data):
        if not hasattr(self, '_capture_data'):
            self._capture_data = False

        if self._capture_data:
            tokens = self._parse_data(data)
            self._code_similarities[self._url].append(tokens)

    def handle_endtag(self, tag):
        self._capture_data = False

class MossRecord:

    def filename(self) -> str:
        return self._filename
    def student_id1(self) -> str:
        return self._student_id1

def parse_moss_html(html) -> Mapping[str, MossRecord]:
    parser = MossHTMLParser()

    print(html)
    parser.feed(html)

    student_records = dict()

    for url, results in parser._code_similarities.items():

        match_parser = MossMatchParser()
        match_parser._base_url = '/'.join(url.split('/')[:-1])
        match_parser.feed(requests.get(url).content.decode())

        if not len(match_parser._codes) == 2:
            raise Exception(str(match_parser._codes))
        code1 = match_parser._codes[0]
        code2 = match_parser._codes[1]

        print(url, results)
        ts1, ts2 = results

        student_id1, filename1, percent1, code_block_slices1 = ts1
        student_id2, filename2, percent2, code_block_slices2 = ts2

    """
    moss_records = [MossStudentPlagiarismRecord(student_id, records) for (student_id, records) in
                    student_records.items()]
    """

    return moss_records

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
        """Gets meta attributes attached pre-parsing."""
        # TODO: Give warning when attaching metadata with name in [code, filename, code_block_slices]
        if name.startswith('self_'):
            return __getattr(self._self, name.removeprefix('self_'))
        elif name.startswith('other_'):
            return __getattr(self._other, name.removeprefix('other_'))
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
    @abstractmethod
    def get_similarities(self, self_filename: str) -> List[MossSimilarity]
        """Returns the similarities of the program with filename "self_filename"."""

