from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets, routers
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

from .serializers import UserSerializer
from rest_framework.generics import GenericAPIView
from account.serializers import AccountSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer


class RegisterView(GenericAPIView):
    """
    Register Api View
    """
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.save(password=make_password(request.data['password1']), is_active=True)
        account_seriallizer = AccountSerializer(data={})
        account_seriallizer.is_valid(raise_exception=True)
        account_seriallizer.save(owner=user_obj)

        return Response({"detail": "User created"}, status=status.HTTP_201_CREATED)


