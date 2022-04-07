from rest_framework import serializers
from referral_sys.models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['invite_code', 'phone_number', 'invited_by']