import uuid 
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.db import models
from django.db.models import Subquery, OuterRef
from datetime import datetime, date
from django.db.models.manager import BaseManager
import pytz

EXCHANGE_NAME = (
     ("EUR", "EUR - euro"),
     ("USD", "USD - dolar"),
     ("GBP", "GBP - funt brytyjski"),
     ("CHF", "CHF - frank szwajcarski")
     )
# Create your models here.
class Exchange(models.Model):
     
     id = models.UUIDField( 
          primary_key = True, 
          default = uuid.uuid4, 
          editable = False) 
     name = models.CharField(max_length=3, choices=EXCHANGE_NAME)
     value = models.FloatField(max_length=250)
     date = models.DateField(editable= True)
     createdOn = models.DateTimeField(auto_now_add=True)
     modifiedOn = models.DateTimeField(auto_now_add=True)

def getData(dateQuery:date)-> BaseManager[Exchange]:
     exchange = Exchange.objects.filter(date__range=[dateQuery, datetime.today().date()])
     return exchange

def getDataByName(dateQuery:date, nameQuery:str)->BaseManager[Exchange]:
     print(dateQuery, nameQuery)
     exchange = Exchange.objects.filter(date__range=[dateQuery, datetime.today().date()], name=nameQuery)
     return exchange

def getDataByDate(dateQuery:date, nameQuery:str)->BaseManager[Exchange]:
     exchange = Exchange.objects.filter(date=dateQuery, name=nameQuery)
     return exchange