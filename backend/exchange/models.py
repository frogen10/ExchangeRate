import uuid 
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.db import models
from django.db.models import Subquery, OuterRef
from datetime import datetime, date
from django.db.models.manager import BaseManager
import pytz

EXCHANGE_TYPE =  (
     ("mid", "MID - średnia"),
     ("bid", "BID - kupno"),
     ("ask", "ASK - sprzedaż"),
)

EXCHANGE_NAME = (
     ("PLN", "Polish zloty"),
     ("EUR", "Euro"),
     ("USD", "American dollar"),
     ("GBP", "British pound"),
     ("CHF", "Swiss franc"),
     )
# Create your models here.
class Exchange(models.Model):
     name = models.CharField(max_length=3, choices=EXCHANGE_NAME)
     currency = models.CharField(max_length=250, null=False, editable=False)
     midValue = models.FloatField(max_length=250, null=True)
     bidValue = models.FloatField(max_length=250, null=True)
     askValue = models.FloatField(max_length=250, null=True)
     date = models.DateTimeField(editable= True)
     createdOn = models.DateTimeField(auto_now_add=True)
     modifiedOn = models.DateTimeField(auto_now_add=True)
     
     def save(self, *args, **kwargs):
        # Set the currency based on the name
        for i in EXCHANGE_NAME:
               if self.name == i[0]:
                    self.currency = i[1]
                    break
        super().save(*args, **kwargs)

     def __str__(self):
        return self.name +" "+self.date.strftime(r'%Y-%m-%d')

def getData(dateQuery:date)-> BaseManager[Exchange]:
     exchange = Exchange.objects.filter(date__range=[dateQuery, datetime.today().date()])
     return exchange

def getDataByName(dateQuery:date, nameQuery:str)->BaseManager[Exchange]:
     print(dateQuery, nameQuery)
     exchange = Exchange.objects.filter(date__range=[dateQuery, datetime.today().date()], name=nameQuery)
     return exchange

def getDataByTypeName(nameQuery:str, top:int)->BaseManager[Exchange]:
     exchange = Exchange.objects.filter(name=nameQuery).order_by('-date')[:top]
     return exchange

def getData(top:int)->BaseManager[Exchange]:
     print(top)
     exchange = []
     for i in EXCHANGE_NAME:
          exchange2 = Exchange.objects.filter(name=i[0]).order_by('-date')[:top]
          exchange.extend(exchange2)
     return exchange


def getDataByDate(dateQuery:date, nameQuery:str)->BaseManager[Exchange]:
     exchange = Exchange.objects.filter(date=dateQuery, name=nameQuery)
     return exchange