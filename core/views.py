from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from .models import Book, Category, Cart, CartItem, Order, OrderItem, User, Author
from .forms import UserRegistrationForm, UserLoginForm, BookForm, UserForm, CategoryForm, AuthorForm

def home(request):
    books = Book.objects.filter(stock_quantity__gt=0)[:8]
    categories = Category.objects.all()[:6]
    
    # Ajouter le nombre d'articles dans le panier
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(cart__user=request.user).count()
    
    return render(request, 'core/home.html', {
        'books': books,
        'categories': categories,
        'cart_count': cart_count
    })

def book_list(request):
    books = Book.objects.filter(stock_quantity__gt=0)
    category_id = request.GET.get('category')
    search_query = request.GET.get('search')
    
    if category_id:
        books = books.filter(category_id=category_id)
    
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__name__icontains=search_query) |
            Q(isbn__icontains=search_query)
        )
    
    categories = Category.objects.all()
    return render(request, 'core/book_list.html', {
        'books': books,
        'categories': categories
    })

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'core/book_detail.html', {'book': book})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to BookHub.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'core/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Incorrect username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserLoginForm()
    return render(request, 'core/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    # Vérifier le stock
    if book.stock_quantity <= 0:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'This book is out of stock.'})
        messages.error(request, 'This book is out of stock.')
        return redirect('book_detail', book_id=book_id)
    
    # Récupérer ou créer le panier
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Ajouter ou mettre à jour l'article du panier
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, 
        book=book,
        defaults={'quantity': 1}
    )
    
    message = ''
    if not created:
        # Vérifier si la nouvelle quantité ne dépasse pas le stock
        if cart_item.quantity + 1 <= book.stock_quantity:
            cart_item.quantity += 1
            cart_item.save()
            message = f'Quantity updated for {book.title}.'
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': f'Insufficient stock for {book.title}.'})
            messages.warning(request, f'Insufficient stock for {book.title}.')
            return redirect('book_detail', book_id=book_id)
    else:
        message = f'{book.title} has been added to your cart.'
    
    # Calculer le nombre total d'articles dans le panier
    cart_count = CartItem.objects.filter(cart=cart).count()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True, 
            'message': message,
            'cart_count': cart_count
        })
    
    messages.success(request, message)
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        total = sum(item.book.price * item.quantity for item in cart_items)
    except Cart.DoesNotExist:
        cart_items = []
        total = 0
    
    return render(request, 'core/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart_count = CartItem.objects.filter(cart__user=request.user).count()
        return JsonResponse({'success': True, 'cart_count': cart_count})
    
    messages.success(request, 'Item removed from cart.')
    return redirect('cart_detail')

@login_required
def update_cart_quantity(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity <= 0:
            cart_item.delete()
            message = 'Item removed from cart.'
        elif quantity <= cart_item.book.stock_quantity:
            cart_item.quantity = quantity
            cart_item.save()
            message = 'Quantity updated.'
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Insufficient stock.'})
            messages.error(request, 'Insufficient stock.')
            return redirect('cart_detail')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            cart_count = CartItem.objects.filter(cart__user=request.user).count()
            cart_items = CartItem.objects.filter(cart__user=request.user)
            total = sum(item.book.price * item.quantity for item in cart_items)
            return JsonResponse({
                'success': True, 
                'message': message,
                'cart_count': cart_count,
                'total': float(total)
            })
        
        messages.success(request, message)
    
    return redirect('cart_detail')

def get_cart_count(request):
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(cart__user=request.user).count()
        return JsonResponse({'cart_count': cart_count})
    return JsonResponse({'cart_count': 0})

def live_search(request):
    query = request.GET.get('q', '').strip()
    if len(query) < 1:
        return JsonResponse({'books': []})
    
    books = Book.objects.filter(
        Q(title__icontains=query) |
        Q(author__name__icontains=query) |
        Q(isbn__icontains=query),
        stock_quantity__gt=0
    )[:10]
    
    books_data = []
    for book in books:
        books_data.append({
            'id': book.id,
            'title': book.title,
            'author': book.author.name,
            'price': float(book.price),
            'cover_image': book.cover_image.url if book.cover_image else None
        })
    
    return JsonResponse({'books': books_data})

@login_required
def my_orders(request):
    # Récupérer les livres achetés (commandes)
    purchased_books = OrderItem.objects.filter(order__user=request.user).select_related('book', 'order')
    
    # Récupérer les livres dans le panier
    cart_books = []
    try:
        cart = Cart.objects.get(user=request.user)
        cart_books = CartItem.objects.filter(cart=cart).select_related('book')
    except Cart.DoesNotExist:
        pass
    
    return render(request, 'core/my_orders.html', {
        'purchased_books': purchased_books,
        'cart_books': cart_books
    })

@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        
        if not cart_items:
            messages.warning(request, 'Your cart is empty.')
            return redirect('cart_detail')
        
        total = sum(item.book.price * item.quantity for item in cart_items)
        
    except Cart.DoesNotExist:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart_detail')
    
    if request.method == 'POST':
        import time
        import random
        
        time.sleep(1)
        payment_success = random.random() < 0.95
        
        if payment_success:
            order = Order.objects.create(
                user=request.user,
                total_amount=total,
                status='completed'
            )
            
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    book=item.book,
                    quantity=item.quantity,
                    price=item.book.price
                )
                
                item.book.stock_quantity -= item.quantity
                item.book.save()
            
            cart_items.delete()
            
            messages.success(request, f'Payment successful! Order #{order.id} confirmed.')
            return render(request, 'core/payment_success.html', {'order': order})
        else:
            messages.error(request, 'Payment failed. Please try again.')
    
    return render(request, 'core/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })

# Admin Panel Views
def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.role == 'admin')

@user_passes_test(is_admin)
def admin_panel(request):
    users_count = User.objects.count()
    books_count = Book.objects.count()
    orders_count = Order.objects.count()
    categories_count = Category.objects.count()
    
    return render(request, 'core/admin_panel.html', {
        'users_count': users_count,
        'books_count': books_count,
        'orders_count': orders_count,
        'categories_count': categories_count
    })

@user_passes_test(is_admin)
def admin_users(request):
    users = User.objects.all().order_by('-created_at')
    return render(request, 'core/admin_users.html', {'users': users})

@user_passes_test(is_admin)
def admin_add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully!')
            return redirect('admin_users')
    else:
        form = UserForm()
    return render(request, 'core/admin_add_user.html', {'form': form})

@user_passes_test(is_admin)
def admin_books(request):
    books = Book.objects.all().order_by('-created_at')
    return render(request, 'core/admin_books.html', {'books': books})

@user_passes_test(is_admin)
def admin_add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            form = BookForm()
            return render(request, 'core/admin_add_book.html', {'form': form})
    else:
        form = BookForm()
    return render(request, 'core/admin_add_book.html', {'form': form})

@user_passes_test(is_admin)
def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'core/admin_orders.html', {'orders': orders})

from django.views.decorators.csrf import csrf_exempt

@user_passes_test(is_admin)
@csrf_exempt
def admin_delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})