from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import BalanceViewSet, TransactionViewSet

router = DefaultRouter()
router.register("transactions", TransactionViewSet, basename="transactions")
router.register("balance", BalanceViewSet, basename="balance")
urlpatterns = [
    path('', include(router.urls)),
]
