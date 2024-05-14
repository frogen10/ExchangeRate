from django.shortcuts import render
from exchange.email import Plot
import mpld3
from rest_framework import viewsets, status, decorators
from .serializers import ExchangeSerializer, ChartSerializer
from .chart import Chart
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Exchange, EXCHANGE_NAME, getDataByTypeName, getData, getDataByName
import logging
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
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
        fromCurrency =self.request.GET.get("from")
        toCurrency = self.request.GET.get("to")
        day = self.request.GET.get("day")
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
        elif(fromCurrency != None and toCurrency != None and day != None):
            now = datetime.now().date()
            DAYS = {
                "1D": (now - timedelta(hours=24)),
                "1W": (now - timedelta(days=7)),
                "1M": (now - timedelta(days=30)),
                "1Y": (now - relativedelta(years=1)),
                "5Y": (now - relativedelta(years=5)),
            }
            date = DAYS[day]
            fromCurrency = getDataByName(date, fromCurrency)
            toCurrency = getDataByName(date, toCurrency)
            minLen = min(len(fromCurrency), len(toCurrency))
            for i in range(minLen):
                fromCurrency[i].midValue = round((1 * fromCurrency[i].askValue / toCurrency[i].bidValue), 4)
                fromCurrency[i].bidValue = round((1 * fromCurrency[i].askValue / toCurrency[i].bidValue), 4)
                fromCurrency[i].askValue = round((1 * fromCurrency[i].askValue / toCurrency[i].bidValue), 4)
            self.queryset = fromCurrency
        return self.queryset
    
class ChartViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = ChartSerializer
    queryset = [Chart("PLN", "EUR","1D")]

    def get_queryset(self):
        logger.debug("querySet")
        fromCurrency =self.request.GET.get("from")
        toCurrency = self.request.GET.get("to")
        day = self.request.GET.get("day")
        if(fromCurrency != None and toCurrency != None and day != None):
            self.queryset[0] = Chart(fromCurrency, toCurrency, day)
        return self.queryset