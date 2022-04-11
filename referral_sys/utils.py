import random
import time


class ThirdPartySMSCodeProviderMockup(object):

    @classmethod
    def get_code(cls):
        time.sleep(random.randint(1, 3))
        return str(random.randint(1000, 9999))


class InviteCodeProviderMockup(object):

    @classmethod
    def get_invite_code(cls):
        return str(random.randint(100_000, 999_999))