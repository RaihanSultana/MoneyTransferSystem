from django.contrib import admin
from .models import Account, Transaction


class AccountModelAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'account_balance',)
    list_editable = ('account_balance',)


class TransactionModelAdmin(admin.ModelAdmin):
    list_display = ('from_account', 'to_account', 'amount')


admin.site.register(Account, AccountModelAdmin)
admin.site.register(Transaction, TransactionModelAdmin)
