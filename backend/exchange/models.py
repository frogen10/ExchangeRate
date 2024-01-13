import uuid 
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.db import models
from django.db.models import When, Case
from datetime import datetime


# Create your models here.
class Exchange(models.Model):
     EXCHANGE_NAME = (
          ("PLN", "PLN - złoty"),
          ("EUR", "EUR - euro"),
          ("USD", "USD - dolar"),
          ("GBP", "GBP - funt brytyjski"),
          ("CHF", "CHF - frank szwajcarski")
          )
     id = models.UUIDField( 
          primary_key = True, 
          default = uuid.uuid4, 
          editable = False) 
     name = models.CharField(max_length=3, choices=EXCHANGE_NAME)
     value = models.FloatField(max_length=250)
     date = models.DateTimeField(editable= True)
     createdOn = models.DateTimeField(auto_now_add=True)
     modifiedOn = models.DateTimeField(auto_now_add=True)
     
     @classmethod
     def create(cls, name:str, value:float, date:datetime):
          exchange = cls(name=name, value=value, date=date)
          # do something with the book
          return exchange
     
     @classmethod
     def get(cls, date:datetime):
          exchange = cls.objects.filter(datetime_published__year=date.year, 
                         datetime_published__month=date.month, 
                         datetime_published__day=date.day)
          # do something with the book
          return exchange

Exchange.get = staticmethod(Exchange.get)