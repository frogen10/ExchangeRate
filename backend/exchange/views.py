from django.shortcuts import render
from exchange.email import Plot
import mpld3
from rest_framework import viewsets
from .serializers import ExchangeSerializer
from .models import Exchange

# Create your views here.
def index(req):
    plot = Plot()
    g = mpld3.fig_to_html(plot.GetPlot())
    
    context = {'g': g}
    return render(req, 'graph.html', context)


class ExchangeViewSet(viewsets.ModelViewSet):
    serializer_class = ExchangeSerializer
    queryset = Exchange.objects.all()
    
    def get_queryset(self):
        return self.queryset