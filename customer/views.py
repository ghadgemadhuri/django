from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from customer.models import Customers
from customer.serializers import CustomersSerializer
import json

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the customer index.") 

@csrf_exempt
def customer_list(request):
	if request.method == 'GET':
		customer = Customers.objects.all()
		serializer = CustomersSerializer(customer, many=True)
		return JsonResponse(serializer.data, safe=False)

	elif request.method == 'POST':
		#print(request.body)
		#data = JSONParser().parse(request.body)
		#data=request.body
		body_unicode = request.body
		body = json.loads(body_unicode)
		print(body)
		serializer = CustomersSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def customer_detail(request, pk):
    try:
         customers = Customers.objects.get(pk=pk)
    except Customers.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CustomersSerializer(customers)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CustomersSerializer(customers, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        customer.delete()
        return HttpResponse(status=204)

