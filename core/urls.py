from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('cart/add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/count/', views.get_cart_count, name='get_cart_count'),
    path('live-search/', views.live_search, name='live_search'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('checkout/', views.checkout, name='checkout'),
    # Admin Panel URLs
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/users/', views.admin_users, name='admin_users'),
    path('admin-panel/users/add/', views.admin_add_user, name='admin_add_user'),
    path('admin-panel/books/', views.admin_books, name='admin_books'),
    path('admin-panel/books/add/', views.admin_add_book, name='admin_add_book'),
    path('admin-panel/orders/', views.admin_orders, name='admin_orders'),
    path('admin-panel/users/delete/<int:user_id>/', views.admin_delete_user, name='admin_delete_user'),
]