import requests

from .moss_report import MossReport
from .concrete_moss_report import ConcreteMossReport
from .concrete_moss_similarity import ConcreteMossSimilarity
from .moss_html_parser import MossHTMLParser, MossMatchParser
from .moss_report_factory import MossReportFactory

class ConcreteMossReportFactory(MossReportFactory):

    def create_moss_report(self, moss_html_report: str) -> MossReport:

        parser = MossHTMLParser()

        parser.feed(moss_html_report)

        filenames_to_similarities: Mapping[str, MossSimilarity] = dict()

        for url, results in parser._code_similarities.items():

            match_parser = MossMatchParser()
            match_parser._base_url = '/'.join(url.split('/')[:-1])
            match_parser.feed(requests.get(url).content.decode())

            code1, code2 = match_parser._codes[0], match_parser._codes[1]

            ts1, ts2 = results

            filename1, percent1, code_block_slices1 = ts1
            filename2, percent2, code_block_slices2 = ts2

            class Record:
                def __init__(self, code, filename, percent_similar, code_block_slices):
                    self.code = code
                    self.filename = filename
                    self.percent_similar = percent_similar
                    self.code_block_slices = code_block_slices

            item_1 = Record(code1, filename1, percent1, code_block_slices1)
            item_2 = Record(code2, filename2, percent2, code_block_slices2)




            similarities = filenames_to_similarities.get(filename1, None) or []
            similarities.append(ConcreteMossSimilarity(self=item_1, other=item_2))
            filenames_to_similarities[filename1] = similarities

            similarities = filenames_to_similarities.get(filename2, None) or []
            similarities.append(ConcreteMossSimilarity(self=item_2, other=item_1))
            filenames_to_similarities[filename2] = similarities

        print(filenames_to_similarities.items())
        return ConcreteMossReport(filenames_to_similarities)
