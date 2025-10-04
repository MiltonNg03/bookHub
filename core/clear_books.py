import os
import sys
import django

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BookHub.settings')
django.setup()

from core.models import Category, Author, Book

def clear_all_books():
    print("Deleting all books...")
    
    books_count = Book.objects.count()
    authors_count = Author.objects.count()
    categories_count = Category.objects.count()
    
    print(f"Before deletion:")
    print(f"  - {books_count} books")
    print(f"  - {authors_count} authors")
    print(f"  - {categories_count} categories")
    
    Book.objects.all().delete()
    print("✓ All books deleted")
    
    Author.objects.all().delete()
    print("✓ All authors deleted")
    
    Category.objects.all().delete()
    print("✓ All categories deleted")
    
    print("\nDeletion complete! The database is now empty.")

if __name__ == "__main__":
    confirmation = input("Are you sure you want to delete ALL books? (yes/no): ")
    if confirmation.lower() in ['yes', 'y', 'oui', 'o']:
        clear_all_books()
    else:
        print("Deletion cancelled.")