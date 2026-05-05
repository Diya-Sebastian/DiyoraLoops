from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('SELLER', 'Seller'),
        ('CUSTOMER', 'Customer'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CUSTOMER')

    def is_admin(self):
        return self.role == 'ADMIN' or self.is_superuser
    
    def is_seller(self):
        return self.role == 'SELLER'
    
    def is_customer(self):
        return self.role == 'CUSTOMER'
