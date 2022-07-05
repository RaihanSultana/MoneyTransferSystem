from django.urls import path, include
from .models import User
from rest_framework import serializers, viewsets, routers
from django.db.models import Q


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(style={'input_type': 'password'}, required=True, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, required=True, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'phone', 'is_active', 'first_name', 'last_name', 'password1', 'password2']

    def validate(self, data):
        phone = data.get("phone", "")
        username = data.get("username", "")
        password1 = data.pop('password1')
        password2 = data.pop('password2')

        phone_qs = User.objects.filter(Q(phone=phone))
        username_qs = User.objects.filter(Q(username=username))
        if phone_qs.exists():
            raise serializers.ValidationError("Phone number already exists.")
        if username_qs.exists():
            raise serializers.ValidationError("Username already exists.")
        if password1 != password2:
            raise serializers.ValidationError("Passwords didn't match.")

        return data


