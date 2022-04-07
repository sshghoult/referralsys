from django.db import models


# Create your models here.
class ProfileManager(models.Manager):
    def get_user(self, invite_code):
        return self.get_queryset().filter(invite_code=invite_code)

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
