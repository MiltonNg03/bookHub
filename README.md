# BookHub

An online bookstore platform built with Django.

## Features

- **User Management**: Registration, login, customer and admin profiles
- **Book Catalog**: Browse by categories, search, book details
- **Shopping Cart**: Add/remove items, quantity management
- **Orders**: Complete ordering process with status tracking
- **Admin Panel**: Manage books, users and orders

## Technologies Used

- **Backend**: Django 4.2.7
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Images**: Pillow for image handling

## Installation

1. Clone the project:
```bash
git clone <repo-url>
cd bookHub
```

2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Start the server:
```bash
python manage.py runserver
```

## Project Structure

```
bookHub/
├── BookHub/          # Django configuration
├── core/             # Main application
│   ├── models.py     # Models (User, Book, Order, etc.)
│   ├── views.py      # Views
│   ├── templates/    # HTML templates
│   └── static/       # CSS files
├── media/            # Uploaded images
└── manage.py         # Django management script
```

## Main Models

- **User**: Users with roles (customer/admin)
- **Book**: Books with author, category, price, stock
- **Category**: Book categories
- **Author**: Book authors
- **Cart/CartItem**: Shopping cart
- **Order/OrderItem**: Orders and order items

## Usage

1. Go to `http://127.0.0.1:8000/`
2. Create an account or login
3. Browse the book catalog
4. Add books to cart
5. Place your order

## Administration

Access the admin panel at `/admin/` with your superuser credentials to:
- Manage books and categories
- View orders
- Administer users