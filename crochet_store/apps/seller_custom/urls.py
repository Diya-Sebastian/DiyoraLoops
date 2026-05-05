from django.urls import path
from . import views

app_name = 'seller_custom'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('products/', views.manage_products, name='manage_products'),
    path('products/add/', views.add_product, name='add_product'),
    path('orders/', views.view_orders, name='view_orders'),
    path('custom-requests/', views.custom_requests, name='custom_requests'),
]
