from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

class UserAbstractSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserAuthorizationSerializer(UserAbstractSerializer):
    pass


class UserRegistrationSerializer(UserAbstractSerializer):
    pass

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError('User already exists!')


class UserCodeSerializer(serializers.Serializer):
    code = serializers.IntegerField(min_value=6)