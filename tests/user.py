
from pyfeatures.storage import User


class UserTester(User):

    def __init__(self, user_id, *, groups=[]):
        self.user_id = user_id
        self.groups = groups

    def get_id(self):
        return self.user_id

    def is_in_groups(self, groups):
        for group in groups:
            if group in self.groups:
                return True
        return False
