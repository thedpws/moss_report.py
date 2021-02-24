from typing import List, Mapping
from .moss_report import MossReport, MossSimilarity


class ConcreteMossReport(MossReport):

    def __init__(self, filenames_to_similarities: Mapping[str, List[MossSimilarity]]):
        self._filenames_to_similarities = filenames_to_similarities

    def get_similarities(self, self_filename: str) -> List[MossSimilarity]:
        return self._filenames_to_similarities[self_filename]

