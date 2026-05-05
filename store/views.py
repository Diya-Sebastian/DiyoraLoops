from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
import json
from .models import Product, Category, Order, OrderItem, CustomerProfile, CustomOrder, Review
from .forms import ProductForm, CategoryForm, CustomerProfileForm
from django.contrib.auth import get_user_model
from accounts.forms import CustomUserCreationForm
User = get_user_model()

# --- Role Checkers ---
def is_admin(user):
    return user.is_authenticated and user.is_admin()

def is_seller(user):
    return user.is_authenticated and user.is_seller()

def is_customer(user):
    return user.is_authenticated and user.is_customer()

# --- Customer Views ---
def home(request):
    products = Product.objects.all()[:4]
    return render(request, 'store/home.html', {'products': products})

def shop(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
        
    return render(request, 'store/shop.html', {'products': products, 'categories': categories})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

@login_required
def cart(request):
    if request.user.is_customer():
        order, created = Order.objects.get_or_create(customer=request.user, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    return render(request, 'store/cart.html', {'items': items, 'order': order})

@login_required
def checkout(request):
    if request.user.is_customer():
        order, created = Order.objects.get_or_create(customer=request.user, complete=False)
        items = order.orderitem_set.all()
        
        if request.method == 'POST':
            order.complete = True
            order.save()
            return redirect('home')
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    return render(request, 'store/checkout.html', {'items': items, 'order': order})

@login_required
def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
        
    return JsonResponse('Item was added', safe=False)

@login_required
def profile(request):
    profile, created = CustomerProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        if 'cancel_order_id' in request.POST:
            order_id = request.POST.get('cancel_order_id')
            order = Order.objects.filter(id=order_id, customer=request.user, complete=True).first()
            if order and order.status in ['Order Placed', 'Processing', 'Packed']:
                order.status = 'Cancelled'
                order.save()
            return redirect('profile')
            
        form = CustomerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomerProfileForm(instance=profile)
        
    orders = Order.objects.filter(customer=request.user, complete=True).order_by('-date_ordered')
    return render(request, 'store/profile.html', {'form': form, 'orders': orders})

@login_required
def request_custom(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        image = request.FILES.get('image')
        
        CustomOrder.objects.create(
            customer=request.user,
            request_description=description,
            reference_image=image
        )
        return redirect('profile')
        
    return render(request, 'store/request_custom.html')

@login_required
def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        Review.objects.create(
            product=product,
            customer=request.user,
            rating=int(rating),
            comment=comment
        )
    return redirect('product_detail', pk=pk)

# --- Admin Views ---
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_products = Product.objects.count()
    total_customers = User.objects.filter(role='CUSTOMER').count()
    total_orders = Order.objects.filter(complete=True).count()
    revenue = sum([order.get_cart_total for order in Order.objects.filter(complete=True)])
    
    recent_orders = Order.objects.filter(complete=True).order_by('-date_ordered')[:5]
    
    # Mock data for the last 7 days of revenue to pass to Chart.js
    chart_labels = json.dumps(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    chart_data = json.dumps([250, 400, 150, 600, 450, 800, float(revenue) if revenue > 0 else 0])
    
    context = {
        'total_products': total_products,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'revenue': revenue,
        'recent_orders': recent_orders,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }
    return render(request, 'admin/dashboard.html', context)

@user_passes_test(is_admin)
def admin_products(request):
    products = Product.objects.all()
    
    if request.method == 'POST':
        if 'delete' in request.POST:
            product_id = request.POST.get('product_id')
            Product.objects.get(id=product_id).delete()
            return redirect('admin_products')
        
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_products')
    else:
        form = ProductForm()
        
    return render(request, 'admin/products.html', {'products': products, 'form': form})

@user_passes_test(is_admin)
def admin_edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_products')
    else:
        form = ProductForm(instance=product)
        
    return render(request, 'admin/edit_product.html', {'form': form, 'product': product})

@user_passes_test(is_admin)
def admin_categories(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_categories')
    else:
        form = CategoryForm()
        
    return render(request, 'admin/categories.html', {'categories': categories, 'form': form})

@user_passes_test(is_admin)
def admin_users(request):
    users = User.objects.all()
    
    if request.method == 'POST':
        if 'delete' in request.POST:
            user_id = request.POST.get('user_id')
            User.objects.get(id=user_id).delete()
            return redirect('admin_users')
            
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_users')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'admin/users.html', {'users': users, 'form': form})

@user_passes_test(is_admin)
def admin_orders(request):
    orders = Order.objects.filter(complete=True).order_by('-date_ordered')
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        status = request.POST.get('status')
        order = Order.objects.get(id=order_id)
        order.status = status
        order.save()
        return redirect('admin_orders')
        
    return render(request, 'admin/orders.html', {'orders': orders})

# --- Seller Views ---
@user_passes_test(is_seller)
def seller_dashboard(request):
    my_products_count = Product.objects.filter(seller=request.user).count()
    my_orders = OrderItem.objects.filter(product__seller=request.user, order__complete=True).order_by('-date_added')
    low_stock = Product.objects.filter(seller=request.user, stock__lt=5)
    
    context = {
        'my_products_count': my_products_count,
        'recent_orders': my_orders[:5],
        'low_stock': low_stock,
    }
    return render(request, 'seller/dashboard.html', context)

@user_passes_test(is_seller)
def seller_products(request):
    products = Product.objects.filter(seller=request.user)
    
    if request.method == 'POST':
        if 'delete' in request.POST:
            product_id = request.POST.get('product_id')
            Product.objects.get(id=product_id, seller=request.user).delete()
            return redirect('seller_products')
            
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('seller_products')
    else:
        form = ProductForm()
        
    return render(request, 'seller/products.html', {'products': products, 'form': form})

@user_passes_test(is_seller)
def seller_edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('seller_products')
    else:
        form = ProductForm(instance=product)
        
    return render(request, 'seller/edit_product.html', {'form': form, 'product': product})

@user_passes_test(is_seller)
def seller_orders(request):
    order_items = OrderItem.objects.filter(product__seller=request.user, order__complete=True).order_by('-date_added')
    
    if request.method == 'POST':
        order_idx = request.POST.get('order_id')
        status = request.POST.get('status')
        # Update the overarching order status
        # In a real system, order items might have individual statuses, 
        # but here we update the main order containing the seller's product.
        order = Order.objects.get(id=order_idx)
        order.status = status
        order.save()
        return redirect('seller_orders')
        
    return render(request, 'seller/orders.html', {'order_items': order_items})

@user_passes_test(is_seller)
def seller_custom_orders(request):
    custom_orders = CustomOrder.objects.all().order_by('-date_requested')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        order_id = request.POST.get('order_id')
        custom_order = get_object_or_404(CustomOrder, id=order_id)
        
        if action == 'quote':
            price = request.POST.get('quoted_price')
            if price:
                custom_order.quoted_price = price
                custom_order.seller = request.user
                custom_order.save()
        elif action == 'accept':
            custom_order.is_accepted = True
            custom_order.status = 'Design Planning'
            custom_order.seller = request.user
            custom_order.save()
        elif action == 'status_update':
            status = request.POST.get('status')
            if status:
                custom_order.status = status
                custom_order.save()
        
        return redirect('seller_custom_orders')
        
    return render(request, 'seller/custom_orders.html', {'custom_orders': custom_orders})
