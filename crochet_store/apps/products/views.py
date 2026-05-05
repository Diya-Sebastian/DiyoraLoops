from django.shortcuts import render, get_object_or_404
from .models import Product, Wishlist

def home_view(request):
    products = Product.objects.all()[:6] # Show some products on home page
    return render(request, 'products/home.html', {'products': products})

def product_list_view(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

def wishlist_view(request):
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        wishlist_items = []
    return render(request, 'products/wishlist.html', {'wishlist_items': wishlist_items})
