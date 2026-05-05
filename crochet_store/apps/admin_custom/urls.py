from django.urls import path
from . import views

app_name = 'admin_custom'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('users/', views.manage_users, name='manage_users'),
    path('users/toggle/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('sellers/', views.approve_sellers, name='approve_sellers'),
    path('sellers/approve/<int:user_id>/', views.approve_seller, name='approve_seller'),
    path('products/', views.manage_products, name='manage_products'),
    path('orders/', views.view_orders, name='view_orders'),
    path('analytics/', views.sales_analytics, name='sales_analytics'),
    path('disputes/', views.handle_disputes, name='handle_disputes'),
]
