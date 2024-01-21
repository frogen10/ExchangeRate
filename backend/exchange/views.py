from django.shortcuts import render
from exchange.email import Plot

# Create your views here.
def index(req):
    plot = Plot()
    g = plot.GetPlot()
    
    context = {'g': g}
    return render(req, 'graph.html', context)