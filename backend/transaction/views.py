from django.shortcuts import render

from rest_framework import viewsets 

from .serializers import BalanceSerializer, TransactionSerializer
from .models import Balance, Transaction

from django.core.exceptions import PermissionDenied

class BalanceViewSet(viewsets.ModelViewSet):
    serializer_class = BalanceSerializer
    queryset = Balance.objects.all()

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        obj = self.get_object()

        if self.request.user != obj.created_by:
            raise PermissionDenied('Wrong object owner')
    
        serializer.save()

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        obj = self.get_object()

        if self.request.user != obj.created_by:
            raise PermissionDenied('Wrong object owner')
    
        serializer.save()