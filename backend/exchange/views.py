from django.shortcuts import render
from . import email
import random  
import matplotlib.pyplot as plt
import mpld3

# Create your views here.
def index(req):
    days=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
    priceOneValues=[]
    for i in range(30):
        priceOneValues.append(random.uniform(4.01, 4.43))
    priceSecondValues=[]
    for i in range(30):
        priceSecondValues.append(random.uniform(3.91, 4.14))
    fig, ax = plt.subplots()
    ax.plot(days, priceOneValues)
    ax.plot(days, priceSecondValues)
    ax.set(xlabel='Dzień tygodnia', ylabel='Cena',
           title='Kursy walut')
    ax.grid()
    g = mpld3.fig_to_html(fig)
    context = {'g': g}
    return render(req, 'graph.html', context)

def FinMinAndMax(Array):
    max = None
    min = None
    for liczba in Array:
        if max is None or liczba > max:
            max = liczba
        if min is None or liczba < min:
            min = liczba
    return max, min