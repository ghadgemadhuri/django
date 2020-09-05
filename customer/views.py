from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from customer.models import Customers
from customer.serializers import CustomersSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
import datetime
import jwt
from django.conf import settings
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import AllowAny
from django.forms import model_to_dict



import json

from rest_framework import viewsets

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
		body_unicode = request.body
		body = json.loads(body_unicode)
		serializer = CustomersSerializer(data=body)
		if serializer.is_valid():
			serializer.save()
			return HttpResponse('created', status=201)
		return HttpResponse('Something went wrong', status=400)

@csrf_exempt
def customer_detail(request, pk):
    try:
         customers = Customers.objects.get(pk=pk)
    except Customers.DoesNotExist:
        return HttpResponse('Customer Not found', status=404)

    if request.method == 'GET':
        serializer = CustomersSerializer(customers)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        body_unicode = request.body
        body = json.loads(body_unicode)
        serializer = CustomersSerializer(customers, data=body)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        customers.delete()
        return HttpResponse(status=204)


class CustomersViewSet(viewsets.ViewSet): 

    def list(self, resquest):
        queryset = Customers.objects.all()
        serializer = CustomersSerializer(queryset, many = True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = Customers.objects.all()
        customer = get_object_or_404(queryset, pk=pk)
        serializer = CustomersSerializer(customer)
        return Response(serializer.data)
    
    def create(self, request): 
        data = json.loads(request.body)
        serializer = CustomersSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def update(self, request, pk=None):
        try:
            customers = Customers.objects.get(pk=pk)
        except Customers.DoesNotExist:
            return HttpResponse('Customer Not found', status=404)
        body_unicode = request.body
        body = json.loads(body_unicode)
        serializer = CustomersSerializer(customers, data=body)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            customers = Customers.objects.get(pk=pk)
        except Customers.DoesNotExist:
            return HttpResponse('Customer Not found', status=404)
        customers.delete()
        return HttpResponse(status=204)

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    response = Response()
    if (username is None) or (password is None):
        raise exceptions.AuthenticationFailed(
            'username and password required')
    user = authenticate(username= username, password = password)
    if user is not None:
        serialized_user = model_to_dict(user)
        token = get_token(user)
        response.data = {
        'access_token': token,
        'user': serialized_user,
        }
        return response
    else:
        return Response(data={'error': 'user not found'}, status=404)

def get_token(user):
    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
    return access_token
