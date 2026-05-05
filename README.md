# DiyoraLoops - Crochet Store Management System

A full-stack, comprehensive web application built with Django, tailored for a crochet business. It features role-based authentication with three distinct modules: Admin, Seller, and Customer, each paired with their own dedicated dashboards.

## Features
- **Admin Module:** Business overview, revenue tracking, user management, order processing, category, and catalog management.
- **Seller Module:** Inventory management, product listing (CRUD), and personal order tracking.
- **Customer Module:** E-commerce shop, cart functionality, checkout processing, and profile/order history viewing.
- **Premium Design System:** A completely custom, vanilla CSS glassmorphism UI replacing standard Bootstrap/Tailwind.

## Requirements
- Python 3.9+
- MySQL Server (optional for out-of-the-box run, strongly recommended for production)
- See `requirements.txt`

## MySQL Setup Instructions

By default, the application is configured to use `sqlite3` for immediate testing and verification without needing a database server right away.
To switch to MySQL as requested:

1. Create a MySQL database locally:
   ```sql
   CREATE DATABASE diyoraloops_db;
   ```
2. Open `diyoraloops/settings.py`.
3. Locate the `DATABASES` setting and comment out the sqlite3 configuration.
4. Uncomment the MySQL configuration:
   ```python
   import pymysql
   pymysql.install_as_MySQLdb()
   
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'diyoraloops_db',
           'USER': 'root',
           'PASSWORD': 'YOUR_MYSQL_PASSWORD', # Update this
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```
5. Apply migrations to the new database:
   ```bash
   python manage.py migrate
   ```

## Demo Data Installation
To immediately populate Categories, Products, and Users (Admin, Seller, Customer), run the custom management command we have provided:

```bash
python manage.py load_demo_data
```

**Demo Accounts Created:**
- Admin: `admin` / `adminpass`
- Seller: `seller` / `sellerpass`
- Customer: `customer` / `customerpass`

## Running the Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000`
