from django.urls import path, include
from customer import views
from . import views
from rest_framework.routers import DefaultRouter
from .views import CustomersViewSet

router = DefaultRouter()
router.register('cust', CustomersViewSet, basename="cust")
urlpatterns = [
    path('', views.index, name='index'),
    path('api/v2/', include(router.urls)),
    path('customer/',views.customer_list),
    path('api/login/',views.login, name='login'),
    path('customer/<int:pk>/', views.customer_detail),
]
