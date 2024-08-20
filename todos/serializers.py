from rest_framework import serializers
from .models import Profile, Todo
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id", "username", "email", "password"]
        extra_kwargs={"passowrd":{"write_only":True}}

    def create(self, validated_data):
        instance=self.Meta.model(**validated_data)
        password=validated_data.pop("password", None)
        if password!=None:
            instance.set_password(password)
            instance.save()
            return instance

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields="__all__"

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Todo
        fields="__all__"