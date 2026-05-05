import os
from io import BytesIO
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.base import ContentFile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from .models import Invoice

def send_order_confirmation_email(user_email, order_id):
    subject = f'Order Confirmation - {order_id}'
    message = f'Thank you for your order! Your order ID is {order_id}. We will notify you once it is shipped.'
    from_email = settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') else 'noreply@diyoraloops.com'
    send_mail(subject, message, from_email, [user_email], fail_silently=True)

def send_payment_success_email(user_email, order_id, amount):
    subject = f'Payment Successful - {order_id}'
    message = f'We have received your payment of ₹{amount} for order {order_id}.'
    from_email = settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') else 'noreply@diyoraloops.com'
    send_mail(subject, message, from_email, [user_email], fail_silently=True)

def send_status_update_email(user_email, order_id, status):
    subject = f'Order Status Update - {order_id}'
    message = f'Your order {order_id} status has been updated to: {status}.'
    from_email = settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') else 'noreply@diyoraloops.com'
    send_mail(subject, message, from_email, [user_email], fail_silently=True)

def generate_invoice_pdf(order):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    p.setFont("Helvetica-Bold", 20)
    p.drawString(200, 750, "DiyoraLoops Invoice")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, 700, f"Order ID: {order.order_id}")
    p.drawString(50, 680, f"Date: {order.created_at.strftime('%Y-%m-%d')}")
    p.drawString(50, 660, f"Customer: {order.user.get_full_name() or order.user.username}")
    
    y = 600
    p.drawString(50, y, "Item Details:")
    y -= 20
    for item in order.items.all():
        product_name = item.product.name if item.product else "Custom Request"
        p.drawString(50, y, f"{product_name} x {item.quantity}")
        p.drawString(400, y, f"₹{item.price}")
        y -= 20
    
    p.line(50, y-10, 500, y-10)
    y -= 30
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Total Amount:")
    p.drawString(400, y, f"₹{order.total_amount}")
    
    p.showPage()
    p.save()
    
    pdf_value = buffer.getvalue()
    buffer.close()
    
    # Save to invoice model
    invoice = Invoice(order=order)
    invoice.pdf_file.save(f'invoice_{order.order_id}.pdf', ContentFile(pdf_value))
    invoice.save()
    
    return invoice
