from django.contrib import admin
from .models import Product, Review, Wishlist

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'created_by')
    list_filter = ('category', 'created_by')
    search_fields = ('name', 'description')

admin.site.register(Review)
admin.site.register(Wishlist)
