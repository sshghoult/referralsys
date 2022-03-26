from rest_framework import views, generics
from rest_framework import mixins
from rest_framework.response import Response

from referral_sys.models import Profile
from .serializers import UserSerializer


# Create your views here.
class UserAPIView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'invite_code'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    # TODO: make model request by hand and move away from Generic



class ProfileAPIView(views.APIView):

    def get(self, request, *args, **kwargs):
        user = Profile.objects.filter(invite_code=kwargs['invite_code'])
        return Response(user)
