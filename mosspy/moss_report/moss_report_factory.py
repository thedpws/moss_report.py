from abc import ABC, abstractmethod
from .moss_report import MossReport

class MossReportFactory(ABC):

    @abstractmethod
    def create_moss_report(self, moss_html_report: str) -> MossReport:
        """Parses the Moss HTML and produces an instance of MossReport"""
