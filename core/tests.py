from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Category, Author, Book

User = get_user_model()

class BookModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Fiction")
        self.author = Author.objects.create(name="John Doe")
        self.book = Book.objects.create(
            title="Test Book",
            author=self.author,
            category=self.category,
            isbn="1234567890123",
            description="Test description",
            price=29.99,
            stock_quantity=10
        )

    def test_book_creation(self):
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.price, 29.99)

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('testpass123'))