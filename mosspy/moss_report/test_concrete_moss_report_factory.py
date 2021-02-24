import unittest

from .concrete_moss_report_factory import ConcreteMossReportFactory
from unittest.mock import Mock, patch

class MossReportFactoryTests(unittest.TestCase):

    def test_creates_moss_report(self):
        # Arrange
        with open('moss.html', 'r') as f:
            moss_html: str = f.read()
        # Act
        moss_report = ConcreteMossReportFactory().create_moss_report(moss_html)
        # Assert
        print(moss_report.get_similarities('main1.c'))

