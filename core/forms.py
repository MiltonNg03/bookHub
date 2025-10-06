from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Book, Category, Author

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', })
    )
    phone_number = forms.CharField(
        max_length=15, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', })
    )
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Adress', 'rows': 3})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'address', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'phone_number', 'address']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if self.cleaned_data['role'] == 'admin':
            user.is_superuser = True
            user.is_staff = True
        else:
            user.is_superuser = False
            user.is_staff = False
        if commit:
            user.save()
        return user

class BookForm(forms.ModelForm):
    author_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    category_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Or enter new category'}))
    
    class Meta:
        model = Book
        fields = ['title', 'isbn', 'description', 'price', 'stock_quantity']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control'})
        }
    
    def save(self, commit=True):
        from .utils import create_book_cover
        import random
        
        print(f"Form data: {self.data}")
        print(f"Cleaned data: {self.cleaned_data}")
        
        # Get author
        author_name = self.cleaned_data.get('author_name')
        print(f"Author name: {author_name}")
        if not author_name:
            raise ValueError("Author name is required")
        author, created = Author.objects.get_or_create(name=author_name)
        print(f"Author: {author} (created: {created})")
        
        # Get category from dropdown
        selected_category = self.data.get('selected_category')
        print(f"Selected category: {selected_category}")
        if not selected_category:
            raise ValueError("Please select a category")
        category, created = Category.objects.get_or_create(name=selected_category)
        print(f"Category: {category} (created: {created})")
        
        # Create book instance
        book = super().save(commit=False)
        book.author = author
        book.category = category
        
        # Generate ISBN if not provided
        if not book.isbn:
            book.isbn = f"9{random.randint(100000000000, 999999999999)}"
        
        print(f"Book before save: {book.title} - {book.author} - {book.category}")
        
        if commit:
            book.save()
            print(f"Book saved with ID: {book.id}")
            # Generate cover
            try:
                cover_path = create_book_cover(book.title, author_name, category.name, book.isbn)
                book.cover_image = cover_path
                book.save()
                print(f"Cover created: {cover_path}")
            except Exception as e:
                print(f"Error creating cover: {e}")
        
        return book

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'bio']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
        }