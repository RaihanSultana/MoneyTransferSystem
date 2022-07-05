from django.db import models
from user.models import User



class Account(models.Model):
    """
    Stores a single account entry, related to :model:'user.User'
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")
    account_balance = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.owner.username


class Transaction(models.Model):
    """
    Stores a single Transaction History, related to :model:'account.Account'
    """
    # owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="transactions")
    from_account = models.ForeignKey(Account, on_delete=models.DO_NOTHING, related_name="money_sent")
    to_account = models.ForeignKey(Account, on_delete=models.DO_NOTHING, related_name="money_received")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
