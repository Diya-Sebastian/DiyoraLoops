from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('seller', 'Seller'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    
    # We can override email to make it unique as requested
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
