# 🧶 DiyoraLoops: A Premium Crochet Marketplace

DiyoraLoops is a production-ready, full-stack e-commerce platform specifically designed for crochet artisans and enthusiasts. It bridges the gap between skilled creators and customers through a specialized custom-order workflow, real-time tracking, and role-based management.

---

## 🚀 Live Demo
**URL**: [http://16.112.129.193](http://16.112.129.193)  
*(Note: Replace with your final domain name once DNS propagation is complete)*

---

## ✨ Key Features

### 👤 User Roles
- **Customers**: Browse products, manage carts, request custom crochet designs, track orders in real-time, and report disputes.
- **Artisans (Sellers)**: Manage product inventory (CRUD), provide price quotes for custom requests, and update order fulfillment statuses.
- **Administrators**: Verify sellers, monitor platform analytics, manage user accounts, and resolve disputes.

### 🛠 Core Functionalities
- **Custom Order Pipeline**: A unique 7-stage workflow (Requested -> Priced -> Accepted -> In Progress -> Ready -> Shipped -> Delivered).
- **Admin Analytics**: Visual dashboards using Chart.js to track revenue and user growth.
- **Dispute Resolution**: Integrated feedback loop for customer satisfaction and quality control.
- **Responsive Design**: Modern, mobile-first UI with a curated "Blue & Pink" aesthetic.

---

## 💻 Tech Stack

- **Backend**: Python 3.x, Django 6.0
- **Database**: AWS RDS (MySQL)
- **Frontend**: Bootstrap 5, JavaScript, Vanilla CSS
- **Infrastructure**: AWS EC2 (Ubuntu 24.04), Nginx, Gunicorn
- **CI/CD**: GitHub Actions (Automated Deployment)
- **Security**: SSL/TLS (Let's Encrypt), Role-Based Access Control (RBAC)

---

## 📂 Project Structure

```text
DiyoraLoops/
├── apps/
│   ├── users/          # Authentication & Role Management
│   ├── products/       # Product CRUD & Catalog
│   ├── orders/         # Cart, Checkout, Custom Requests & Disputes
│   ├── admin_custom/   # Admin Dashboards & Analytics
│   └── seller_custom/  # Artisan Dashboard & Order Fulfillment
├── crochet_store/      # Main Project Configuration
├── static/             # CSS, JS, and Image Assets
├── templates/          # HTML Templates (MVT)
└── manage.py           # Django Management Script
```

---

## 🛠 Installation & Local Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/DiyoraLoops.git
   cd DiyoraLoops
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the server**:
   ```bash
   python manage.py runserver
   ```

---

## 🛡 License
This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author
**Diya Sebastian**  
*Full Stack Developer & Crochet Enthusiast*
