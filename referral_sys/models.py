from django.db import models
from django.shortcuts import get_object_or_404
import referral_sys.utils as utils
import redis
import config.settings as settings
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

from django.core.exceptions import ObjectDoesNotExist

# Create your models here.



class IntegratedProfileManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, **extra_fields):
        if not phone_number:
            raise ValueError('Phone number must be set')
        invite_code = utils.InviteCodeProviderMockup.get_invite_code()
        user = self.model(phone_number=phone_number, invite_code=invite_code, **extra_fields)
        user.save()
        return user

    def create_user(self, phone_number, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, **extra_fields)

    def create_superuser(self, phone_number, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone_number, **extra_fields)

    def get_user_by_code_public(self, invite_code):
        return get_object_or_404(self.get_queryset(), invite_code=invite_code)

    def get_user_by_phone_internal(self, phone_number):
        try:
            user = self.get_queryset().get(phone_number=phone_number)
        except ObjectDoesNotExist:
            user = None

        return user

    def get_referrals(self, invite_code):
        return self.get_queryset().filter(invited_by=invite_code)


class IntegratedProfile(AbstractBaseUser, PermissionsMixin):
    invite_code = models.CharField(max_length=6, unique=True)
    password = models.CharField(max_length=42, null=True, blank=True)
    phone_number = models.CharField(max_length=12, primary_key=True)
    invited_by = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = IntegratedProfileManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['phone_number']

    def get_full_name(self):
        return f"{self.phone_number} - {self.invite_code}"

    def get_short_name(self):
        return self.phone_number



class SMSCodesManagerRedis(object):
    redis_db = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0,
                                 charset="utf-8", decode_responses=True)
    code_timeout = None

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
