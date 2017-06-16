
import unittest
import uuid

from .user import UserTester

from pyrollout.feature import Feature, ALL, NONE


class TestFeature(unittest.TestCase):

    def test_create_empty_feature(self):
        feature = Feature("test")
        self.assertEqual(feature.name, "test")

    def test_create_empty_feature_no_name(self):
        with self.assertRaises(TypeError):
            feature = Feature()

    def test_feature_repr(self):
        feature = Feature("name", users=["user"], groups=["group"])
        self.assertEqual(repr(feature), "Feature('name', groups=['group'])")

    def test_feature_str(self):
        feature = Feature("name", users=["user"], groups=["group"])
        self.assertEqual(str(feature), "<Feature name - Users:['user'] Groups:['group']>")

    def test_create_feature_with_groups(self):
        feature = Feature("test", groups=["test-group"])
        self.assertEqual(feature.groups, ["test-group"])

    def test_create_feature_with_users(self):
        feature = Feature("test", users=["test-user-id"])
        self.assertEqual(feature.users, ["test-user-id"])

    def test_create_feature_percentage(self):
        feature = Feature("test", percentage=50)
        self.assertEqual(feature.percentage, 50)

    def test_create_feature_percentage_randomized(self):
        feature = Feature("test", percentage=50, randomize=True)
        self.assertEqual(feature.percentage, 50)
        self.assertTrue(feature.randomize)

    def test_feature_groups_all_precedence(self):
        with self.assertRaises(AssertionError):
            feature = Feature("test", groups=[ALL, NONE])

    def test_feature_can_group(self):
        regular_dude = UserTester("regular-dude")
        vip_dude = UserTester("vip-dude", groups=["vips"])

        feature_all = Feature("all-feature", groups=[ALL])
        feature_none = Feature("none-feature", groups=[NONE])
        feature_vip = Feature("vip-feature", groups=["vips"])

        # Make sure all users can access the all features
        self.assertTrue(feature_all.can_group(regular_dude))
        self.assertTrue(feature_all.can_group(vip_dude))

        # Make sure no users can access the none features
        self.assertFalse(feature_none.can_group(regular_dude))
        self.assertFalse(feature_none.can_group(vip_dude))

        # Make sure only users in specific groups can access grouped features
        self.assertFalse(feature_vip.can_group(regular_dude))
        self.assertTrue(feature_vip.can_group(vip_dude))

    def test_feature_can_users_by_id(self):
        dude_1 = UserTester("1")
        dude_2 = UserTester("2")
        dude_3 = UserTester("3")

        feature_all = Feature("all-feature", users=["1", "2", "3"])
        feature_none = Feature("none-feature", users=["4"])
        feature_some = Feature("some-feature", users=["1", "3"])

        # Make sure all users can access the all feature
        self.assertTrue(feature_all.can_user(dude_1))
        self.assertTrue(feature_all.can_user(dude_2))
        self.assertTrue(feature_all.can_user(dude_3))

        # Make sure no users can access the none feature
        self.assertFalse(feature_none.can_user(dude_1))
        self.assertFalse(feature_none.can_user(dude_2))
        self.assertFalse(feature_none.can_user(dude_3))

        # Make sure only users 1 and 3 can access the some feature
        self.assertTrue(feature_some.can_user(dude_1))
        self.assertFalse(feature_some.can_user(dude_2))
        self.assertTrue(feature_some.can_user(dude_3))

    def test_feature_can_percentage(self):
        dude_1 = UserTester(1)
        dude_2 = UserTester(40)
        dude_3 = UserTester(50)
        dude_4 = UserTester(99)
        dude_5 = UserTester(uuid.UUID("76aebbea-f25c-4d34-a920-f3077395ef8e"))
        dude_6 = UserTester(uuid.UUID("4f537c77-0fd5-4504-b2e9-d3dd9836b159"))
        dude_7 = UserTester("8b1d9f42-e9c3-4405-8ccc-309a76020960")
        dude_8 = UserTester("606f72b8-c71a-4170-a129-6b89f257bcd8")

        feature10 = Feature("feature10", percentage=10)
        feature45 = Feature("feature45", percentage=45)
        feature60 = Feature("feature60", percentage=60)

        # Make sure that the first 10% of sequential user ids can access the
        # feature.
        self.assertTrue(feature10.can_percentage(dude_1))
        self.assertFalse(feature10.can_percentage(dude_2))
        self.assertFalse(feature10.can_percentage(dude_3))
        self.assertFalse(feature10.can_percentage(dude_4))
        self.assertTrue(feature10.can_percentage(dude_5))
        self.assertFalse(feature10.can_percentage(dude_6))
        self.assertTrue(feature10.can_percentage(dude_7))
        self.assertFalse(feature10.can_percentage(dude_8))

        # Make sure that the first 45% of sequential user ids can access the
        # feature.
        self.assertTrue(feature45.can_percentage(dude_1))
        self.assertTrue(feature45.can_percentage(dude_2))
        self.assertFalse(feature45.can_percentage(dude_3))
        self.assertFalse(feature45.can_percentage(dude_4))
        self.assertTrue(feature10.can_percentage(dude_5))
        self.assertFalse(feature10.can_percentage(dude_6))
        self.assertTrue(feature10.can_percentage(dude_7))
        self.assertFalse(feature10.can_percentage(dude_8))

        # Make sure that the first 60% of sequential user ids can access the
        # feature.
        self.assertTrue(feature60.can_percentage(dude_1))
        self.assertTrue(feature60.can_percentage(dude_2))
        self.assertTrue(feature60.can_percentage(dude_3))
        self.assertFalse(feature60.can_percentage(dude_4))
        self.assertTrue(feature10.can_percentage(dude_5))
        self.assertFalse(feature10.can_percentage(dude_6))
        self.assertTrue(feature10.can_percentage(dude_7))
        self.assertFalse(feature10.can_percentage(dude_8))

    def test_feature_can_percentage_with_random(self):
        dude_1 = UserTester(1)
        dude_2 = UserTester(40)
        dude_3 = UserTester(50)
        dude_4 = UserTester(99)
        dude_5 = UserTester(uuid.UUID("76aebbea-f25c-4d34-a920-f3077395ef8e"))
        dude_6 = UserTester(uuid.UUID("4f537c77-0fd5-4504-b2e9-d3dd9836b159"))
        dude_7 = UserTester("8b1d9f42-e9c3-4405-8ccc-309a76020960")
        dude_8 = UserTester("606f72b8-c71a-4170-a129-6b89f257bcd8")

        feature = Feature("test-feature", percentage=50, randomize=True)

        self.assertTrue(feature.can_percentage(dude_1))
        self.assertFalse(feature.can_percentage(dude_2))
        self.assertFalse(feature.can_percentage(dude_3))
        self.assertTrue(feature.can_percentage(dude_4))
        self.assertTrue(feature.can_percentage(dude_5))
        self.assertFalse(feature.can_percentage(dude_6))
        self.assertTrue(feature.can_percentage(dude_7))
        self.assertTrue(feature.can_percentage(dude_8))

    def test_feature_can(self):
        user_id = UserTester("A")
        user_group = UserTester("B", groups=["group"])

        feature_by_id = Feature("byid", users=["A"])
        feature_by_group = Feature("bygroup", groups=["group"])

        self.assertTrue(feature_by_id.can(user_id))
        self.assertFalse(feature_by_id.can(user_group))

        self.assertFalse(feature_by_group.can(user_id))
        self.assertTrue(feature_by_group.can(user_group))
