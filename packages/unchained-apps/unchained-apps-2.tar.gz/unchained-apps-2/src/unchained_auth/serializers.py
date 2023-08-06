from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from unchained_auth.models import User


class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            "email",
            "password"
        ]


class GoogleUIDSerializer(serializers.Serializer):
    # This can be uid when using phone login or google login
    token = serializers.CharField(
        max_length=4096, required=True, trim_whitespace=True)
