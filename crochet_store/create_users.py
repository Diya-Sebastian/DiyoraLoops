import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crochet_store.settings')
django.setup()

from apps.users.models import User

def create_extra_users():
    # Create Superuser (Admin)
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@diyoraloops.com',
            password='adminpassword',
            role='admin'
        )
        print("Admin created: admin / adminpassword")
    
    # Create Customer
    if not User.objects.filter(username='customer1').exists():
        customer = User.objects.create_user(
            username='customer1',
            email='customer1@example.com',
            password='password123',
            role='customer'
        )
        print("Customer created: customer1 / password123")

if __name__ == '__main__':
    create_extra_users()
