import unittest
from unittest.mock import Mock, patch

from .concrete_moss_similarity import ConcreteMossSimilarity


class MossSimilarityTests(unittest.TestCase):

    def test_when_self_or_other_is_missing_a_required_attribute_then_raises_error(self):
        # Arrange
        expected_attributes = ['code', 'filename', 'code_block_slices', 'percent_similar']


        for missing_attr in expected_attributes:
            mock_self = Mock(**{attr: Mock() for attr in expected_attributes})
            mock_other = Mock(**{attr: Mock() for attr in expected_attributes})


            mock_self.__delattr__(missing_attr)

            
            # Act
            def act():
                ConcreteMossSimilarity(mock_self, mock_other)

            # Assert
            self.assertRaises(AttributeError, act)

            mock_self = Mock(**{attr: Mock() for attr in expected_attributes})
            mock_other = Mock(**{attr: Mock() for attr in expected_attributes})

            mock_other.__delattr__(missing_attr)
            
            # Act
            def act():
                ConcreteMossSimilarity(mock_self, mock_other)

            # Assert
            self.assertRaises(AttributeError, act)
                


    def test_when_meta_attributes_are_included_then_are_accessible_via_self_and_other_prefixes(self):
        # Arrange
        class A:
            def __init__(self, meta_attribute):
                self.meta_attribute = meta_attribute
                self.code = Mock()
                self.filename = Mock()
                self.code_block_slices = []
                self.percent_similar = Mock()

        a_self = A(Mock())
        a_other = A(Mock())

        similarity = ConcreteMossSimilarity(self=a_self, other=a_other)

        # Act
        self_meta_attribute = similarity.self_meta_attribute
        other_meta_attribute = similarity.other_meta_attribute

        # Assert
        self.assertEqual(a_self.meta_attribute, self_meta_attribute)
        self.assertEqual(a_other.meta_attribute, other_meta_attribute)

    def test_when_missing_self_or_other_meta_attribute_is_requested_then_raises_error(self):
        # Arrange
        class A:
            def __init__(self, meta_attribute):
                self.meta_attribute = meta_attribute
                self.code = Mock()
                self.filename = Mock()
                self.code_block_slices = []
                self.percent_similar = Mock()

        a_self = A(Mock())
        a_other = A(Mock())

        similarity = ConcreteMossSimilarity(self=a_self, other=a_other)

        # Act
        def act():
            _ = similarity.self_missing_meta_attribute

        # Assert
        self.assertRaises(AttributeError, act)


        # Act
        def act():
            _ = similarity.other_missing_meta_attribute


        # Assert
        self.assertRaises(AttributeError, act)
