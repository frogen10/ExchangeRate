from django.shortcuts import render
from exchange.email import Plot
import mpld3
from rest_framework import viewsets, status, decorators
from .serializers import ExchangeSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Exchange, EXCHANGE_NAME, getDataByTypeName, getData
import logging
logger = logging.getLogger(__name__)

# Create your views here.
def index(req):
    plot = Plot()
    g = mpld3.fig_to_html(plot.GetPlot())
    
    context = {'g': g}
    return render(req, 'graph.html', context)


class ExchangeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = ExchangeSerializer
    queryset = Exchange.objects.all()
    
    def get_queryset(self):
        logger.debug("querySet")
        name =self.request.GET.get("name")
        top = self.request.GET.get("top")
        tops: int
        if(top != None):
            tops = int(top)
            if(tops >0 and name !=""):
                self.queryset = getDataByTypeName(name, tops)
            if(tops >0):
                self.queryset = getData(tops)
        return self.queryset

class ExchangeNowViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = ExchangeSerializer
    queryset = Exchange.objects.all()
    
    def get_queryset(self):
        logger.debug("querySet")
        name =self.request.GET.get("name")
        top = self.request.GET.get("top")
        tops: int
        if(top != None):
            tops = int(top)
            if(tops >0 and name !=""):
                self.queryset = getDataByTypeName(name, tops)
            if(tops >0):
                self.queryset = getData(tops)
        return self.queryset
    
    def perform_create(self, serializer):
        serializer.save()
    
    def perform_update(self, serializer):
        obj = self.get_object()
        serializer.save()