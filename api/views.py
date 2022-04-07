from rest_framework import views, generics
from rest_framework import mixins
from rest_framework.response import Response

from referral_sys.models import Profile
from .serializers import UserSerializer


class ProfileAPIView(views.APIView):

    def get(self, request, *args, **kwargs):
        user = Profile.objects.get_user(kwargs['invite_code'])
        referrals = Profile.objects.get_referrals(kwargs['invite_code'])

        referrals_serialized = [UserSerializer(k).data for k in referrals]
        response = {'user': UserSerializer(user[0]).data, 'referrals': referrals_serialized}

        return Response(response)
