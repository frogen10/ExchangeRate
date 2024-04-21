from django.shortcuts import render

from rest_framework import viewsets 
from django.contrib.auth.models import User
from .serializers import ClientSerializer
from .models import Client 
from rest_framework.permissions import AllowAny

from django.core.exceptions import PermissionDenied
import logging
logger = logging.getLogger(__name__)
class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        obj = self.get_object()

        if self.request.user != obj.created_by:
            raise PermissionDenied('Wrong object owner')
    
        serializer.save()