from rest_framework import serializers, viewsets, routers
from django.db.models import Q

from .models import Account, Transaction
from user.serializers import UserSerializer


class AccountSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'owner', 'account_balance', 'created_at', 'updated_at']


class TransactionSerializer(serializers.ModelSerializer):
    from_account = AccountSerializer(read_only=True)
    to_account = AccountSerializer(read_only=True)

    to_account_id = serializers.ListField(required=False, write_only=True)

    set_time = serializers.BooleanField(write_only=True, required=False)
    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = Transaction
        fields = ['id', 'from_account', 'to_account', 'amount', 'created_at', 'to_account_id',
                  'set_time', 'time']


