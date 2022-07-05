import decimal
import random
import json
from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets, routers
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.db import transaction
from .tasks import send_money_on_scheduled_time
from django_celery_beat.models import IntervalSchedule, PeriodicTask, CrontabSchedule, ClockedSchedule

from .serializers import AccountSerializer, TransactionSerializer
from .models import Account, Transaction

User = get_user_model()


class SendMoneyView(GenericAPIView):
    """
    View to send money
    ::param: amount:int, from_acount_id:int, to_account_id:list(example: ["3", "4"]), time:%Y-%m-%d %H:%M:%S(example: 2022-07-05 12:42:00), set_time: boolean(example: true)

    json_param_sample: {
                            "amount": "10.00",
                            "to_account_id": ["3", "4"],
                            "time": "2022-07-05 12:42:00",
                            "set_time": false
                        }
    """
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        to_account_id_list = request.data.pop('to_account_id')
        set_time = request.data.pop('set_time')
        amount = request.data['amount']
        sender = Account.objects.filter(owner=request.user).first()
        from_account_id = sender.id

        if set_time == True:  # if time is set, then task will be scheduled
            time = request.data.pop('time')
            slug = random.randint(100, 999)  # since PeriodicTask name field is unique
            clocked, _ = ClockedSchedule.objects.get_or_create(
                clocked_time=time
            )  # creating scheduled time
            PeriodicTask.objects.create(
                name=slug,
                task="send_money_on_scheduled_time",
                kwargs=json.dumps(
                    {'from_account_id': from_account_id, 'to_account_id_list': to_account_id_list,
                     "amount": float(amount)}),
                clocked=clocked,
                one_off=True
            )  # creating periodic task using celery to run the task at scheduled time
            return Response({"detail": "Transaction has been scheduled"}, status=status.HTTP_200_OK)
        else:
            time = request.data.pop('time')

            for to_account_id in to_account_id_list:
                if decimal.Decimal(amount) < decimal.Decimal(sender.account_balance):  # check if sender has sufficient amount in account
                    receiver = Account.objects.filter(pk=to_account_id).first()
                    serializer = self.serializer_class(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    with transaction.atomic():
                        sender.account_balance -= decimal.Decimal(amount)
                        receiver.account_balance += decimal.Decimal(amount)
                        sender.save()
                        receiver.save()
                        serializer.save(from_account=sender, to_account=receiver)
                else:
                    raise serializers.ValidationError("Transaction Failed Due to Insufficient Balance")
            return Response({"detail": "All Transaction successfull"}, status=status.HTTP_201_CREATED)


class TransactionHistory(GenericAPIView):
    """ Transaction History """
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_account = Account.objects.filter(owner=request.user.id).first()
        transaction_qs = Transaction.objects.filter(Q(from_account=user_account) | Q(to_account=user_account))
        serializer = self.serializer_class(transaction_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


