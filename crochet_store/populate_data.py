import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crochet_store.settings')
django.setup()

from apps.products.models import Product
from apps.users.models import User
from django.core.files.base import ContentFile
import requests

def populate():
    # Create a seller user
    seller, created = User.objects.get_or_create(
        username='artisan1',
        email='artisan1@example.com',
        defaults={'role': 'seller'}
    )
    if created:
        seller.set_password('password123')
        seller.save()

    # Dummy product data
    products = [
        {
            'name': 'Crochet Amigurumi Doll',
            'category': 'dolls',
            'price': 450.00,
            'description': 'A beautiful handmade amigurumi doll, perfect for kids.',
            'image_url': 'https://plus.unsplash.com/premium_photo-1663127046013-059960010901?q=80&w=2000&auto=format&fit=crop'
        },
        {
            'name': 'Sunflower Bouquet',
            'category': 'bouquets',
            'price': 800.00,
            'description': 'Everlasting crochet sunflower bouquet.',
            'image_url': 'https://images.unsplash.com/photo-1594222082213-6977adabc9fc?q=80&w=2000&auto=format&fit=crop'
        },
        {
            'name': 'Cute Bunny Keychain',
            'category': 'keychains',
            'price': 150.00,
            'description': 'A small and cute bunny keychain for your bags.',
            'image_url': 'https://images.unsplash.com/photo-1582091283414-97a63d77a06a?q=80&w=2000&auto=format&fit=crop'
        }
    ]

    for p_data in products:
        product, created = Product.objects.get_or_create(
            name=p_data['name'],
            defaults={
                'category': p_data['category'],
                'price': p_data['price'],
                'description': p_data['description'],
                'created_by': seller
            }
        )
        if created:
            # Try to fetch and save image
            try:
                response = requests.get(p_data['image_url'])
                if response.status_code == 200:
                    product.image.save(f"{product.name.replace(' ', '_')}.jpg", ContentFile(response.content), save=True)
            except Exception as e:
                print(f"Error saving image for {product.name}: {e}")

    print("Data populated successfully!")

if __name__ == '__main__':
    populate()
