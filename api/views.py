from rest_framework import views, generics
from rest_framework import mixins
from rest_framework.response import Response

from referral_sys.models import Profile, SMSCodes, SMSCodesRedis, IntegratedProfile
from .serializers import UserSerializer


class ProfileAPIView(views.APIView):

    def get(self, request, *args, **kwargs):
        # user = Profile.objects.get_user(kwargs['invite_code'])
        user = IntegratedProfile.objects.get_user_by_code_public(kwargs['invite_code'])
        referrals = IntegratedProfile.objects.get_referrals(kwargs['invite_code'])

        referrals_serialized = [UserSerializer(k).data for k in referrals]
        response = {'user': UserSerializer(user).data, 'referrals': referrals_serialized}

        return Response(response)


class RequestAuthSMSCodeAPIView(views.APIView):

    def post(self, request, *args, **kwargs):
        code = SMSCodesRedis.objects.request_code(phone_number=request.data['phone_number'])
        resp_data = {"code": code}
        return Response(status=200, data=resp_data)


class ConfirmAuthSMSCodeAPIView(views.APIView):

    def post(self, request, *args, **kwargs):
        check = SMSCodesRedis.objects.check_code(phone_number=request.data['phone_number'],
                                                 input_code=request.data['code'])
        if not check:
            resp = Response(status=404)
        else:
            resp = Response(status=200)

        return resp

# {"phone_number": "1", "code": "9303"}
