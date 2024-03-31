from django.db import models
from django.contrib.auth.models import User
from exchange.models import Exchange, EXCHANGE_TYPE

class Transaction(models.Model):
    exchange = models.ForeignKey(Exchange, related_name='exchange', on_delete=models.CASCADE)
    value = models.FloatField(max_length=250)
    created_by = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        result = self.exchange.name +" "
        if(self.exchange.type == EXCHANGE_TYPE[1][0]):
            result += 'buy'
        elif(self.exchange.type == EXCHANGE_TYPE[2][0]):
            result += 'sell'
        result += " "+str(self.value)
        return result

class Balance(models.Model):
    value = models.FloatField(max_length=250)
    created_by = models.ForeignKey(User, related_name='balance', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_by.username + " "+ str(self.value)
