from django.shortcuts import render
from exchange.email import Plot
import mpld3
# Create your views here.
def index(req):
    plot = Plot()
    g = mpld3.fig_to_html(plot.GetPlot())
    
    context = {'g': g}
    return render(req, 'graph.html', context)