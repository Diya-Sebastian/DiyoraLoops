from django.core.management.base import BaseCommand
from accounts.models import User
from store.models import Category, Product

class Command(BaseCommand):
    help = 'Loads initial demo data into the database'

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating demo users...")
        
        # Admin
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
            admin.role = 'ADMIN'
            admin.save()
            
        # Seller
        if not User.objects.filter(username='seller').exists():
            seller = User.objects.create_user('seller', 'seller@example.com', 'sellerpass')
            seller.role = 'SELLER'
            seller.save()
        else:
            seller = User.objects.get(username='seller')
            
        # Customer
        if not User.objects.filter(username='customer').exists():
            customer = User.objects.create_user('customer', 'customer@example.com', 'customerpass')
            customer.role = 'CUSTOMER'
            customer.save()
            
        self.stdout.write("Creating categories and products...")
        
        cat1, _ = Category.objects.get_or_create(name='Amigurumi', slug='amigurumi', description='Cute stuffed yarn toys.')
        cat2, _ = Category.objects.get_or_create(name='Clothing', slug='clothing', description='Handmade crochet clothing.')
        cat3, _ = Category.objects.get_or_create(name='Accessories', slug='accessories', description='Hats, scarves, and more.')
        
        # Products
        if Product.objects.count() == 0:
            Product.objects.create(category=cat1, seller=seller, title='Crochet Bunny', description='A lovely handmade bunny toy for kids.', price=25.00, stock=10)
            Product.objects.create(category=cat2, seller=seller, title='Winter Cardigan', description='Warm and cozy winter cardigan in beige.', price=65.00, stock=5)
            Product.objects.create(category=cat3, seller=seller, title='Bucket Hat', description='Stylish crochet bucket hat with strawberry design.', price=15.00, stock=20)
            
        self.stdout.write(self.style.SUCCESS('Successfully loaded demo data!'))
