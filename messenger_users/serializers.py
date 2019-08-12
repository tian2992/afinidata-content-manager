from .models import UserData, User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class UserDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserData
        exclude = ['created']