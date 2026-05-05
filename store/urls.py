from django.urls import path
from . import views

urlpatterns = [
    # Customer URLs
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.update_item, name='update_item'),
    path('profile/', views.profile, name='profile'),
    path('request-custom/', views.request_custom, name='request_custom'),
    path('add-review/<int:pk>/', views.add_review, name='add_review'),
    
    # Admin URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-users/', views.admin_users, name='admin_users'),
    path('admin-products/', views.admin_products, name='admin_products'),
    path('admin-products/edit/<int:pk>/', views.admin_edit_product, name='admin_edit_product'),
    path('admin-categories/', views.admin_categories, name='admin_categories'),
    path('admin-orders/', views.admin_orders, name='admin_orders'),

    # Seller URLs
    path('seller-dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('seller-products/', views.seller_products, name='seller_products'),
    path('seller-products/edit/<int:pk>/', views.seller_edit_product, name='seller_edit_product'),
    path('seller-orders/', views.seller_orders, name='seller_orders'),
    path('seller-custom-orders/', views.seller_custom_orders, name='seller_custom_orders'),
]
