from django.db import models

# Create your models here.


class Profile(models.Model):
    invite_code = models.CharField(max_length=6, primary_key=True)
    phone_number = models.CharField(max_length=12)
    invited_by = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.invite_code

    class Meta:
        ordering = ['phone_number']

