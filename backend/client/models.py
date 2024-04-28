from django.contrib.auth.models import User
from django.db import models
from transaction.models import Transaction, Balance
from exchange.models import EXCHANGE_NAME

class Client(models.Model):
    number = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    address1 = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=255, blank=True, null=True)
    place = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    default_currency = models.CharField(max_length=3, choices=EXCHANGE_NAME)
    created_by = models.ForeignKey(User, related_name='clients', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the Client object first

        # Set the currency based on the name
        for i in EXCHANGE_NAME:
            try:
                balance, created = Balance.objects.get_or_create(
                    currency=i[0], 
                    created_by=self.created_by, 
                    defaults={'value': 0}
                )
            except Exception:
                pass  # Balance object already exists, so do nothing

    def __str__(self):
        return '%s' % self.created_by.username

