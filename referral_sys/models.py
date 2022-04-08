from django.db import models
from django.shortcuts import get_object_or_404
import referral_sys.utils as utils
import redis
import config.settings as settings


# Create your models here.
class ProfileManager(models.Manager):
    def get_user(self, invite_code):
        return get_object_or_404(self.get_queryset(), invite_code=invite_code)

    def get_referrals(self, invite_code):
        return self.get_queryset().filter(invited_by=invite_code)


class Profile(models.Model):
    objects = ProfileManager()
    invite_code = models.CharField(max_length=6, primary_key=True)
    phone_number = models.CharField(max_length=12)
    invited_by = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.invite_code

    class Meta:
        ordering = ['phone_number']


class SMSCodesManager(models.Manager):

    def request_code(self, phone_number):
        code = utils.ThirdPartySMSCodeProviderMockup.get_code()
        print(self.create(phone_number=phone_number, expected_code=code))
        return code

    def check_code(self, phone_number, input_code):
        row = get_object_or_404(self.get_queryset(), phone_number=phone_number)
        return row.expected_code == input_code


class SMSCodes(models.Model):
    objects = SMSCodesManager()
    expected_code = models.CharField(max_length=4)
    phone_number = models.CharField(max_length=12, primary_key=True)

    def __str__(self):
        return f"{self.phone_number} - {self.expected_code}"


class SMSCodesManagerRedis(object):
    redis_db = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0,
                                 charset="utf-8", decode_responses=True)
    code_timeout = 120

    def request_code(self, phone_number):
        code = utils.ThirdPartySMSCodeProviderMockup.get_code()
        instance_repr = SMSCodesRedis(phone_number, code).redis_repr()
        self.redis_db.set(instance_repr['name'], instance_repr['value'], ex=self.code_timeout)
        return code

    def check_code(self, phone_number, input_code):
        stored_code = self.redis_db.get(phone_number)
        # print(f"{stored_code=}, {input_code=}")
        return stored_code == input_code


class SMSCodesRedis(object):
    objects = SMSCodesManagerRedis()

    def __init__(self, phone_number, expected_code):
        self.phone_number = phone_number
        self.expected_code = expected_code

    def __str__(self):
        return f"{self.phone_number} - {self.expected_code}"

    def json_repr(self):
        return {'phone_number': self.phone_number, 'code': self.expected_code}

    def redis_repr(self):
        return {"name": self.phone_number, "value": self.expected_code}




