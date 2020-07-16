from rest_framework import serializers
from customer.models import Customers,Bill
#from django.contrib.auth.models import user
#from django.contrib.auth.models import authenticate
#from rest_framework import exceptions

"""
class CustomersSerializer(serializers.Serializer):
	customer_id=serializers.AutoField(primary_key=True)
	first_name=serializers.CharField(max_length=30)
	last_name=serializers.CharField(max_length=30)
	address=serializers.TextField(max_length=100)
	email_id=serializers.EmailField(max_length=30)
	mobile_number=serializers.IntegerField()

	def create(self,validated_data):
		return customer.objects.create(**validated_data)

	def update(self,instance,validated_data):
		instance.customer_id=validated_data.get('customer_id',instance.customer_id)


class CustomersSerializer(serializers.ModelSerializer):
	class Meta:
		model = Customers
		fields = ('customer_id','first_name', 'last_name', 'address', 'email_id', 'mobile_number')
"""

class CustomersSerializer(serializers.ModelSerializer):
	class Meta:
		model = Customers
		fields = ('customer_id','first_name', 'last_name', 'address', 'email_id', 'mobile_number')
			
class BillSerializer(serializers.ModelSerializer):
	class Meta:
		model=Bill
		fields=('customers','bill_id','bill_date','amount','discount')

		depth=1




