from django.contrib import admin
from transaction.models import Transaction, Balance
# Register your models here.
admin.site.register(Transaction)
admin.site.register(Balance)