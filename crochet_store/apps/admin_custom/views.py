from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from apps.users.models import User
from apps.products.models import Product
from apps.orders.models import Order, Dispute
from django.db.models import Sum

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'admin':
            return view_func(request, *args, **kwargs)
        messages.error(request, "Access denied. Admin only.")
        return redirect('users:login')
    return wrapper

@login_required
@admin_required
def dashboard(request):
    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.exclude(status='cancelled').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Real Activity Data
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_orders = Order.objects.order_by('-created_at')[:5]
    
    context = {
        'total_users': total_users,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'recent_users': recent_users,
        'recent_orders': recent_orders,
    }
    return render(request, 'admin_custom/dashboard.html', context)

@login_required
@admin_required
def toggle_user_status(request, user_id):
    user = User.objects.get(id=user_id)
    if user == request.user:
        messages.error(request, "You cannot block yourself!")
    else:
        user.is_active = not user.is_active
        user.save()
        status = "unblocked" if user.is_active else "blocked"
        messages.success(request, f"User {user.username} has been {status}.")
    return redirect('admin_custom:manage_users')

@login_required
@admin_required
def edit_user(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        user.email = request.POST.get('email')
        user.role = request.POST.get('role')
        user.save()
        messages.success(request, f"User {user.username} updated successfully.")
        return redirect('admin_custom:manage_users')
    return render(request, 'admin_custom/edit_user.html', {'target_user': user})

@login_required
@admin_required
def manage_users(request):
    users = User.objects.exclude(role='admin')
    return render(request, 'admin_custom/manage_users.html', {'users': users})

@login_required
@admin_required
def approve_seller(request, user_id):
    user = User.objects.get(id=user_id, role='seller')
    user.is_active = True
    user.save()
    
    # Send Notification Email
    subject = "Account Approved - Stitched Warmth"
    message = f"Hello {user.username},\n\nYour artisan account has been approved by the administrator. You can now log in and start managing your products and orders.\n\nLogin here: http://127.0.0.1:9999/users/login/\n\nWelcome to the family!"
    send_mail(subject, message, 'admin@stitchedwarmth.com', [user.email])
    
    messages.success(request, f"Seller {user.username} has been approved and notified.")
    return redirect('admin_custom:approve_sellers')

@login_required
@admin_required
def approve_sellers(request):
    sellers = User.objects.filter(role='seller')
    return render(request, 'admin_custom/approve_sellers.html', {'sellers': sellers})

@login_required
@admin_required
def manage_products(request):
    products = Product.objects.all()
    return render(request, 'admin_custom/manage_products.html', {'products': products})

@login_required
@admin_required
def view_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'admin_custom/view_orders.html', {'orders': orders})

import json
from django.db.models.functions import TruncDate

@login_required
@admin_required
def sales_analytics(request):
    # Sales over time (last 30 days)
    sales_data = Order.objects.exclude(status='cancelled') \
        .annotate(date=TruncDate('created_at')) \
        .values('date') \
        .annotate(total=Sum('total_amount')) \
        .order_by('date')
    
    dates = [d['date'].strftime('%Y-%m-%d') for d in sales_data if d['date']]
    amounts = [float(d['total'] or 0) for d in sales_data]
    
    # User distribution
    customer_count = User.objects.filter(role='customer').count()
    seller_count = User.objects.filter(role='seller').count()
    
    # Dashboard summary data (in case parent template needs it)
    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.exclude(status='cancelled').aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    context = {
        'dates_json': json.dumps(dates),
        'amounts_json': json.dumps(amounts),
        'user_counts': json.dumps([customer_count, seller_count]),
        'total_users': total_users,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
    }
    return render(request, 'admin_custom/analytics.html', context)

@login_required
@admin_required
def handle_disputes(request):
    disputes = Dispute.objects.all().order_by('-created_at')
    return render(request, 'admin_custom/disputes.html', {'disputes': disputes})

@login_required
@admin_required
def update_dispute_status(request, dispute_id):
    if request.method == 'POST':
        status = request.POST.get('status')
        dispute = Dispute.objects.get(id=dispute_id)
        dispute.status = status
        dispute.save()
        messages.success(request, f"Dispute status updated to {dispute.get_status_display()}.")
    return redirect('admin_custom:handle_disputes')
