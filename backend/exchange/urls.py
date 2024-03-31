from django import urls
from django.urls import path, include
from . import views
from .views import ExchangeViewSet
from rest_framework import viewsets

from rest_framework.routers import DefaultRouter

router =DefaultRouter()
router.register("exchange", ExchangeViewSet, basename="exchange")
urlpatterns  = [
    path('graph', views.index, name='graph'),
    path('', include(router.urls))
]