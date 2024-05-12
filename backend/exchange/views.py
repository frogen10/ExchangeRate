from django.shortcuts import render
from exchange.email import Plot
import mpld3
from rest_framework import viewsets, status, decorators
from .serializers import ExchangeSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Exchange, EXCHANGE_NAME, getDataByTypeName, getData
import logging
from datetime import datetime
from random import randint
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
        refresh = self.request.GET.get("refresh")
        period = self.request.GET.get("period")
        tops: int
        if(top != None):
            tops = int(top)
            if(tops >0 and name !=""):
                self.queryset = getDataByTypeName(name, tops)
            if(tops >0):
                self.queryset = getData(tops)
        elif(refresh != None):
            logger.debug("refresh")
            exchange = getData(1)
            for j in exchange:
                exchange2 = Exchange(
                    name=j.name,
                    midValue= round(j.midValue + (j.midValue * randint(-5, 5) / 100), 4),
                    bidValue=round(j.bidValue + (j.bidValue * randint(-5, 5) / 100), 4),
                    askValue=round(j.askValue + (j.askValue * randint(-5, 5) / 100), 4),
                    date=datetime.now(),
                    createdOn=datetime.now(),
                    modifiedOn=datetime.now()
                )
                exchange2.save()
            self.queryset = getData(1)

        elif(period != None):
            pass
        return self.queryset