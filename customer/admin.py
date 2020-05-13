from django.contrib import admin

# Register your models here.

from .models import Customers,Bill
admin.site.register(Customers)
admin.site.register(Bill)
