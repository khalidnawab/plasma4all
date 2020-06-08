from rest_framework.serializers import ModelSerializer
from plasma.models import Profile
"""serializer class for generating json for the Demographics table."""


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
