from django.db import models

# Create your models here.
#from django.db import models


class Customers(models.Model):
    customer_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.TextField(max_length=100)
    email_id = models.EmailField(max_length=30)
    mobile_number = models.IntegerField()
    

class Bill(models.Model):
    customers= models.ForeignKey(Customers,on_delete=models.CASCADE,null=True)
    bill_id = models.AutoField(primary_key=True)
    bill_date = models.DateTimeField(auto_now=True)
    amount = models.FloatField()
    discount = models.FloatField(max_length=100)


