import os
import re
from html.parser import HTMLParser

import requests


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
        filename = os.path.basename(filepath)

        # TODO: implement :)
        code_block_slices: List[Tuple[int, int]] = []

        return filename, percent_similar, code_block_slices

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

