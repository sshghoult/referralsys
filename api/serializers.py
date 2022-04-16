from rest_framework import serializers
from referral_sys.models import IntegratedProfile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegratedProfile
        fields = ['invite_code', 'phone_number', 'invited_by']


class ProfileSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = IntegratedProfile
        fields = ['phone_number']
