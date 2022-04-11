from .models import SMSCodesRedis, IntegratedProfile
from django.contrib.auth.backends import BaseBackend



class SMSCodeBackend(BaseBackend):
    def authenticate(self, request, phone_number=None, input_code=None):
        auth = SMSCodesRedis.objects.check_code(phone_number=phone_number, input_code=input_code)
        if auth:
            user = self.get_user(phone_number)
            if user is None:
                user = IntegratedProfile.objects.create_user(phone_number=phone_number)

            return user

    def get_user(self, phone_number):
        return IntegratedProfile.objects.get_user_by_phone_internal(phone_number)




