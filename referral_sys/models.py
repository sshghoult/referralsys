from django.db import models
from django.shortcuts import get_object_or_404
import referral_sys.utils as utils



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
