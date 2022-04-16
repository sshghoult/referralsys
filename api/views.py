from rest_framework import views, generics
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin
import django.db

from referral_sys.models import SMSCodesRedis, IntegratedProfile
from .serializers import ProfileSerializer, ProfileSerializerShort

from referral_sys.authentication import SMSCodeBackend

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomLoginRequiredMixin(LoginRequiredMixin):
    # login_url = '/api/auth/code_request'
    raise_exception = True


class ProfileAPIView(CustomLoginRequiredMixin, UpdateModelMixin, views.APIView):

    def get(self, request, *args, **kwargs):
        user = IntegratedProfile.objects.get_user_by_code_public(kwargs['invite_code'])
        if user is None:
            return Response(status=404)

        referrals = IntegratedProfile.objects.get_referrals(kwargs['invite_code'])

        referrals_serialized = [ProfileSerializerShort(k).data for k in referrals]
        print(referrals, referrals_serialized)
        response = {'user': ProfileSerializer(user).data, 'referrals': referrals_serialized}

        return Response(response)

    def patch(self, request, *args, **kwargs):
        # TODO: validate damn payloads in middleware!

        user = IntegratedProfile.objects.get_user_by_code_public(kwargs['invite_code'])
        if user is None:
            return Response(status=404)

        invited_by_prof = IntegratedProfile.objects.get_user_by_code_public(
            request.data['invited_by'])
        if invited_by_prof is None:
            return Response(status=404)

        user.invited_by = invited_by_prof

        if request.user.invite_code != kwargs['invite_code']:
            resp = Response(status=403, data={"message": "user can not change data of others"})
        elif request.data['invited_by'] == user.invite_code:
            resp = Response(status=409, data={"message": "user can not be their own referral"})
        else:
            try:
                user.save(update_fields=['invited_by'])
            except django.db.Error as e:
                resp = Response(status=403, data={"message": "faulty payload"})
            else:
                resp = Response(status=204)


        return resp


class WhoAmIView(views.APIView):
    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            data = ProfileSerializer(IntegratedProfile.objects.get_user_by_code_public(
                request.user.invite_code)).data
            return Response(status=200, data=data)
        else:
            return Response(status=404)


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
            data = ProfileSerializer(user).data
            return Response(status=200, data=data)
        else:
            return Response(status=404)

# {"phone_number": "1", "code": "9303"}
# {"invited_by": "234475"}
