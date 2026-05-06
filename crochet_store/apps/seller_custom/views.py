from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.products.models import Product
from apps.orders.models import Order, CustomOrder
from functools import wraps

def seller_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'seller':
            return view_func(request, *args, **kwargs)
        messages.error(request, "Access denied. Seller account required.")
        return redirect('users:login')
    return _wrapped_view

@login_required
@seller_required
def dashboard(request):
    products_count = Product.objects.filter(created_by=request.user).count()
    # Placeholder for actual order logic
    orders_count = 0 
    custom_requests_count = CustomOrder.objects.filter(artisan=request.user).count()
    
    context = {
        'products_count': products_count,
        'orders_count': orders_count,
        'custom_requests_count': custom_requests_count,
    }
    return render(request, 'seller_custom/dashboard.html', context)

from .forms import SellerProductForm

@login_required
@seller_required
def add_product(request):
    if request.method == 'POST':
        form = SellerProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            messages.success(request, f"Product '{product.name}' added successfully!")
            return redirect('seller_custom:manage_products')
    else:
        form = SellerProductForm()
    return render(request, 'seller_custom/add_product.html', {'form': form})

@login_required
@seller_required
def manage_products(request):
    products = Product.objects.filter(created_by=request.user)
    return render(request, 'seller_custom/manage_products.html', {'products': products})

from apps.orders.models import Order, CustomOrder, OrderItem

@login_required
@seller_required
def view_orders(request):
    # Fetch order items that belong to this seller's products
    order_items = OrderItem.objects.filter(product__created_by=request.user).order_by('-order__created_at')
    return render(request, 'seller_custom/orders.html', {'order_items': order_items})

@login_required
@seller_required
def custom_requests(request):
    from django.db.models import Q
    
    if request.method == 'POST':
        action = request.POST.get('action')
        order_id = request.POST.get('order_id')
        # Allow picking unassigned OR managing assigned
        order = get_object_or_404(CustomOrder, Q(order_id=order_id) & (Q(artisan=request.user) | Q(artisan__isnull=True)))
        
        if action == 'claim':
            order.artisan = request.user
            order.save()
            messages.success(request, f"You have claimed Request #{order_id[:8]}.")
        
        elif action == 'quote':
            price = request.POST.get('quoted_price')
            order.total_price = price
            order.status = 'priced'
            order.save()
            messages.success(request, f"Price quote sent for Request.")
        
        elif action == 'accept':
            order.status = "accepted"
            order.save()
            messages.success(request, f"You have accepted the Order.")
            
        elif action == 'status_update':
            new_status = request.POST.get('status')
            order.status = new_status
            order.save()
            messages.success(request, f"Order status updated to {new_status}.")
            
        return redirect('seller_custom:custom_requests')

    # Show requests assigned to them OR unassigned requests
    requests = CustomOrder.objects.filter(Q(artisan=request.user) | Q(artisan__isnull=True)).order_by('-created_at')
    return render(request, 'seller_custom/custom_requests.html', {'custom_orders': requests})

@login_required
@seller_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = SellerProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product '{product.name}' updated successfully!")
            return redirect('seller_custom:manage_products')
    else:
        form = SellerProductForm(instance=product)
    return render(request, 'seller_custom/add_product.html', {'form': form, 'edit_mode': True})

@login_required
@seller_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, created_by=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('seller_custom:manage_products')
    return render(request, 'seller_custom/delete_product_confirm.html', {'product': product})
