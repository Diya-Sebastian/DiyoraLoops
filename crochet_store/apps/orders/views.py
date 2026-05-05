from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.products.models import Product
from .models import Order, CustomOrder

def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for pid, qty in cart.items():
        product = get_object_or_404(Product, pk=pid)
        item_total = product.price * qty
        total += item_total
        cart_items.append({'product': product, 'quantity': qty, 'item_total': item_total})
    
    return render(request, 'orders/cart.html', {'cart_items': cart_items, 'total': total})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    pid = str(product_id)
    if pid in cart:
        cart[pid] += 1
    else:
        cart[pid] = 1
    request.session['cart'] = cart
    return redirect('orders:cart')

def update_cart_quantity(request, product_id, action):
    cart = request.session.get('cart', {})
    pid = str(product_id)
    if pid in cart:
        if action == 'increase':
            cart[pid] += 1
        elif action == 'decrease':
            cart[pid] -= 1
            if cart[pid] <= 0:
                del cart[pid]
    request.session['cart'] = cart
    return redirect('orders:cart')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    pid = str(product_id)
    if pid in cart:
        del cart[pid]
    request.session['cart'] = cart
    return redirect('orders:cart')

@login_required
def checkout_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('products:home')
    
    cart_items = []
    total = 0
    for pid, qty in cart.items():
        product = get_object_or_404(Product, pk=pid)
        item_total = product.price * qty
        total += item_total
        cart_items.append({'product': product, 'quantity': qty, 'item_total': item_total})

    if request.method == 'POST':
        shipping_name = request.POST.get('shipping_name')
        shipping_address = request.POST.get('shipping_address')

        # Create the Order object
        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            shipping_name=shipping_name,
            shipping_address=shipping_address,
            status='pending'
        )
        
        # Create OrderItem objects
        from .models import OrderItem
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['item_total']
            )
        
        # Clear the cart
        request.session['cart'] = {}
        
        from django.contrib import messages
        messages.success(request, f"Order #{str(order.order_id)[:8]} has been placed successfully!")
        return redirect('products:home')

    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items, 
        'total': total
    })

from .forms import CustomOrderRequestForm

@login_required
def custom_order_request_view(request):
    if request.method == 'POST':
        form = CustomOrderRequestForm(request.POST, request.FILES)
        if form.is_valid():
            custom_order = form.save(commit=False)
            custom_order.user_id = request.user
            custom_order.save()
            return redirect('orders:tracking')
    else:
        form = CustomOrderRequestForm()
    return render(request, 'orders/custom_order_form.html', {'form': form})

@login_required
def order_tracking_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    custom_orders = CustomOrder.objects.filter(user_id=request.user).order_by('-created_at')
    return render(request, 'orders/tracking.html', {'orders': orders, 'custom_orders': custom_orders})

@login_required
def artisan_dashboard_view(request):
    if request.user.role != 'seller':
        return redirect('products:home')
    # Basic dashboard logic
    return render(request, 'orders/artisan_dashboard.html')

@login_required
def artisan_custom_requests_view(request):
    if request.user.role != 'seller':
        return redirect('products:home')
    requests = CustomOrder.objects.filter(status='requested')
    return render(request, 'orders/artisan_custom_requests.html', {'requests': requests})
