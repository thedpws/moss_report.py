from .moss_report import MossReport
from .moss_html_parser import MossHTMLParser, MossMatchParser
from .moss_report_factory import MossReportFactory

class ConcreteMossReportFactory(MossReportFactory):

    def create_moss_report(self, moss_html_report: str) -> MossReport:

        parser = MossHTMLParser()

        print(html)
        parser.feed(html)

        filenames_to_similarities: Mapping[str, MossSimilarity] = dict()

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

            filename1, percent1, code_block_slices1 = ts1
            filename2, percent2, code_block_slices2 = ts2

            item_1 = {
                'code'              : code1,
                'filename'          : filename1,
                'code_block_slices' : code_block_slices1,
                'percent_similar'   : percent1,
            }

            item_2 = {
                'code'              : code2,
                'filename'          : filename2,
                'code_block_slices' : code_block_slices2,
                'percent_similar'   : percent2,
            }

            obj_1, obj_2 = object(), object()
            for k,v in item_1.items():
                setattr(obj_1, k, v)
            for k,v in item_2.items():
                setattr(obj_2, k, v)

            similarities = filenames_to_similarities.get(filename1, default=None) or []
            similarities.append(ConcreteMossSimilarity(self=obj_1, other=obj_2))
            filenames_to_similarities.put(filename1, similarities)

            similarities = filenames_to_similarities.get(filename2, default=None) or []
            similarities.append(ConcreteMossSimilarity(self=obj_2, other=obj_1))
            filenames_to_similarities.put(filename2, similarities)

    return ConcreteMossReport(filenames_to_similarities)
