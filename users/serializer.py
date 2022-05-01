from dataclasses import fields
from re import I
from rest_framework import serializers

from users.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = '__all__'
