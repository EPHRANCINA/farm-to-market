from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='list'),
    path('<int:pk>/', views.order_detail, name='detail'),
    path('create/<int:product_pk>/', views.order_create, name='create'),
    path('<int:pk>/cancel/', views.order_cancel, name='cancel'),
] 