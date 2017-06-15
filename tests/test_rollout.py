
import unittest

from .user import UserTester

from pyrollout.rollout import Rollout
from pyrollout.feature import Feature, ALL, NONE
from pyrollout.storage import FeatureStorage
from pyrollout.storage.memory import MemoryStorage


class TestRollout(unittest.TestCase):

    def test_create_default_rollout(self):
        rollout = Rollout()
        self.assertIsInstance(rollout.feature_storage, FeatureStorage)
        self.assertFalse(rollout.undefined_feature_access)

    def test_create_custom_rollout(self):
        class TestStorage(FeatureStorage):
            pass

        rollout = Rollout(feature_storage=TestStorage())
        self.assertIsInstance(rollout.feature_storage, TestStorage)
        self.assertFalse(rollout.undefined_feature_access)

    def test_set_feature(self):
        ms = MemoryStorage()
        feature = Feature("feature")
        rollout = Rollout(feature_storage=ms)
        rollout.set_feature(feature)

        self.assertTrue(feature == ms.feature_data["feature"])

    def test_can(self):
        user = UserTester("A")
        feature = Feature("feature", users=["A"])
        ms = MemoryStorage()
        ms.feature_data = {"feature": feature}
        rollout = Rollout(feature_storage=ms)

        self.assertTrue(rollout.can(user, "feature"))
        self.assertFalse(rollout.can(user, "made-up"))
