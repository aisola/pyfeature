
import unittest

from .user import UserTester

from pyfeatures import Feature, Manager
from pyfeatures.storage import FeatureStorage
from pyfeatures.storage.memory import MemoryStorage


class TestManager(unittest.TestCase):

    def test_create_default_manager(self):
        man = Manager()
        self.assertIsInstance(man.feature_storage, FeatureStorage)
        self.assertFalse(man.undefined_feature_access)

    def test_create_custom_manager(self):
        class TestStorage(FeatureStorage):
            pass

        man = Manager(feature_storage=TestStorage())
        self.assertIsInstance(man.feature_storage, TestStorage)
        self.assertFalse(man.undefined_feature_access)

    def test_set_feature(self):
        ms = MemoryStorage()
        feature = Feature("feature")
        man = Manager(feature_storage=ms)
        man.set_feature(feature)

        self.assertTrue(feature == ms.feature_data["feature"])

    def test_can(self):
        user = UserTester("A")
        feature = Feature("feature", users=["A"])
        ms = MemoryStorage()
        ms.feature_data = {"feature": feature}
        man = Manager(feature_storage=ms)

        self.assertTrue(man.can(user, "feature"))
        self.assertFalse(man.can(user, "made-up"))
