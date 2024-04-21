from django.contrib import admin
from exchange.models import Exchange
# Register your models here.
@admin.register(Exchange)
class MyModelAdmin(admin.ModelAdmin):
    readonly_fields = ('currency','createdOn', 'modifiedOn')
    fields = ('currency', 'name', 'midValue', 'bidValue', 'askValue', 'date', 'createdOn', 'modifiedOn')