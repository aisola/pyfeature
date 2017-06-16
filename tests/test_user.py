
import unittest

from pyfeatures.storage import User


class TestUser(unittest.TestCase):

    def setUp(self):
        self.emptyUser = User()

    def test_get_id(self):
        with self.assertRaises(NotImplementedError):
            self.emptyUser.get_id()

    def test_is_in_groups(self):
        with self.assertRaises(NotImplementedError):
            self.emptyUser.is_in_groups(["fake-group", "notha-one"])
