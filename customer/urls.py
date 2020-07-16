from django.urls import path
from customer import views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('customer/',views.customer_list),
    path('customer/<int:pk>/', views.customer_detail),
    path('bill/',views.bill_list),
    path('bill/<int:pk>/', views.bill_detail),
    path('login/',views.login)
   # path(r'^object/$', csrf_exempt(views.ObjectView.as_view())),
]
