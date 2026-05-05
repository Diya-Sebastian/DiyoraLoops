from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<uuid:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<uuid:product_id>/<str:action>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/remove/<uuid:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    
    path('custom-order/', views.custom_order_request_view, name='custom_order_request'),
    path('tracking/', views.order_tracking_view, name='tracking'),
    
    # Artisan paths
    path('artisan/dashboard/', views.artisan_dashboard_view, name='artisan_dashboard'),
    path('artisan/custom-requests/', views.artisan_custom_requests_view, name='artisan_custom_requests'),
]
