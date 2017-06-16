
import unittest

from pyfeatures import Feature
from pyfeatures.storage import FeatureStorage


class TestFeatureStorage(unittest.TestCase):

    def setUp(self):
        self.storage = FeatureStorage()

    def test_get_feature_by_name(self):
        with self.assertRaises(NotImplementedError):
            self.storage.get_feature_by_name("this-should-totally-fail")

    def test_set_feature(self):
        with self.assertRaises(NotImplementedError):
            self.storage.set_feature(Feature("Hello"))
