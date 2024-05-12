from django.db import models
from django.contrib.auth.models import User
from django.db.models import F
from exchange.models import Exchange, EXCHANGE_TYPE, EXCHANGE_NAME

TRANSACTION_TYPE = (('buy', 'buy'), ('sell', 'sell'))

class Transaction(models.Model):
    type = models.CharField(max_length=255, choices=TRANSACTION_TYPE)
    value = models.FloatField(max_length=250)
    from_currency = models.ForeignKey(Exchange, related_name='from_currency', on_delete=models.CASCADE)
    to_currency = models.ForeignKey(Exchange, related_name='to_currency', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Call the "real" save() method.
        super().save(*args, **kwargs)
        # Decrease the balance of the from_currency.
        Balance.objects.filter(created_by=self.created_by, currency=self.from_currency.name).update(value=F('value') - self.value)
        # Increase the balance of the to_currency.
        Balance.objects.filter(created_by=self.created_by, currency=self.to_currency.name).update(value=round(F('value') + (self.value * self.from_currency.askValue / self.to_currency.bidValue)))

    def __str__(self):
        return str(self.value)+self.from_currency.name +" = "+str(self.value*self.from_currency.bidValue/self.to_currency.askValue)+" "+self.to_currency.name + " " + self.type

class Balance(models.Model):
    value = models.FloatField(max_length=250)
    currency = models.CharField(max_length=3, choices=EXCHANGE_NAME)
    created_by = models.ForeignKey(User, related_name='balance', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_by.username + " "+ str(self.value)
