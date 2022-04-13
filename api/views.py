from rest_framework import views, generics
from rest_framework import mixins
from rest_framework.response import Response

from referral_sys.models import SMSCodesRedis, IntegratedProfile
from .serializers import ProfileSerializer

from referral_sys.authentication import SMSCodeBackend

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomLoginRequiredMixin(LoginRequiredMixin):
    # login_url = '/api/auth/code_request'
    raise_exception = True


class ProfileAPIView(CustomLoginRequiredMixin, views.APIView):

    def get(self, request, *args, **kwargs):
        # user = Profile.objects.get_user(kwargs['invite_code'])
        user = IntegratedProfile.objects.get_user_by_code_public(kwargs['invite_code'])
        referrals = IntegratedProfile.objects.get_referrals(kwargs['invite_code'])

        referrals_serialized = [ProfileSerializer(k).data for k in referrals]
        response = {'user': ProfileSerializer(user).data, 'referrals': referrals_serialized}

        return Response(response)


class RequestAuthSMSCodeAPIView(views.APIView):

    def post(self, request, *args, **kwargs):
        code = SMSCodesRedis.objects.request_code(phone_number=request.data['phone_number'])
        resp_data = {"code": code}
        return Response(status=200, data=resp_data)


class ConfirmAuthSMSCodeAPIView(views.APIView):

    def post(self, request, *args, **kwargs):
        user = SMSCodeBackend().authenticate(request, phone_number=request.data['phone_number'],
                                             input_code=request.data['code'])
        if user is not None:
            login(request, user)
            return Response(status=200)
        else:
            return Response(status=404)

# {"phone_number": "1", "code": "9303"}
