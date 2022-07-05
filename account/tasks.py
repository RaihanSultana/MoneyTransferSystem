from celery import shared_task
import decimal
from django.db import transaction
from rest_framework import serializers
from .models import Account, Transaction


@shared_task(name="send_money_on_scheduled_time")
def send_money_on_scheduled_time(*args, **kwargs):
    """
    function for sending money on scheduled time
    :return: None
    """
    sender_id = kwargs['from_account_id']
    receiver_id_list = kwargs['to_account_id_list']
    amount = kwargs['amount']
    sender = Account.objects.filter(pk=sender_id).first()
    for receiver_id in receiver_id_list:
        receiver = Account.objects.filter(pk=receiver_id).first()
        with transaction.atomic():
            if amount < sender.account_balance:
                with transaction.atomic():
                    sender.account_balance -= decimal.Decimal(amount)
                    receiver.account_balance += decimal.Decimal(amount)
                    sender.save()
                    receiver.save()
                    Transaction.objects.create(from_account=sender, to_account=receiver, amount=amount)
                    print("money sent")

            else:
                print("Transaction Failed Due to Insufficient Balance")
                raise serializers.ValidationError("Transaction Failed Due to Insufficient Balance")
    return None
