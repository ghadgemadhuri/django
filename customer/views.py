#from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from customer.models import Customers,Bill
from customer.serializers import CustomersSerializer,BillSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate	
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the Customer index.") 

@csrf_exempt
def customer_list(request):
	if request.method == 'GET':
		customer = Customers.objects.all()
		serializer = CustomersSerializer(customer, many=True)
		return JsonResponse(serializer.data, safe=False)

	elif request.method == 'POST':
		#print(request.body)
		data = JSONParser().parse(request)
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
             return JsonResponse(serializer.data,200)
         return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        customers.delete()
        return HttpResponse(status=200)
    



@csrf_exempt
def bill_list(request):
	if request.method == 'GET':
		bill = Bill.objects.all()
		serializer = BillSerializer(bill, many=True)
		return JsonResponse(serializer.data, safe=False)

	elif request.method == 'POST':
		#print(request.body)
		data = JSONParser().parse(request)
		serializer = BillSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def bill_detail(request, pk):
    try:
         bill = Bill.objects.get(pk=pk)
    except Bill.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = BillSerializer(bill)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = BillSerializer(bill, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        bill.delete()
        return HttpResponse(status=200)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")	
    if  not  username.strip() or password.strip():
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_400_BAD_REQUEST)
    return Response({'msg':'Login Succesfully'},  status=HTTP_200_OK)



