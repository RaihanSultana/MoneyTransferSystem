from django.urls import path, include
from rest_framework import routers

from .views import SendMoneyView, TransactionHistory

router = routers.DefaultRouter()


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/send_money/', SendMoneyView.as_view()),
    path('api/transaction_history/', TransactionHistory.as_view()),
]

