from django.contrib import admin
from .models import CustomOrder, Order, OrderItem, Invoice

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'total_amount', 'status', 'is_custom')
    list_filter = ('status', 'is_custom')
    inlines = [OrderItemInline]

@admin.register(CustomOrder)
class CustomOrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user_id', 'category', 'status', 'total_price', 'artisan')
    list_filter = ('status', 'category')

admin.site.register(Invoice)
