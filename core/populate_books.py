import os
import sys
import django
import requests
from django.core.files.base import ContentFile
from datetime import datetime

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BookHub.settings')
django.setup()

from core.models import Category, Author, Book
import random

def search_books_by_category(category_name, max_results=10):
    base_url = "https://www.googleapis.com/books/v1/volumes"
    books_data = []
    search_terms = {
        'Fiction': 'fiction',
        'Science Fiction': 'science fiction',
        'Fantasy': 'fantasy',
        'Mystery': 'mystery',
        'Biography': 'biography',
        'Self Help': 'self help'
    }
    
    search_query = search_terms.get(category_name, 'books')
    
    params = {
        'q': search_query,
        'maxResults': max_results,
        'printType': 'books'
    }
    
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            
            for item in data.get('items', []):
                volume_info = item.get('volumeInfo', {})
                
                if not volume_info.get('title') or not volume_info.get('authors'):
                    continue
                
                thumbnail = volume_info.get('imageLinks', {}).get('thumbnail')
                if not thumbnail:
                    thumbnail = volume_info.get('imageLinks', {}).get('smallThumbnail')
                
                book_data = {
                    'title': volume_info.get('title', 'Unknown Title'),
                    'authors': volume_info.get('authors', ['Unknown Author']),
                    'description': volume_info.get('description', f'An excellent {category_name.lower()} book.'),
                    'isbn': None,
                    'thumbnail': thumbnail,
                    'page_count': volume_info.get('pageCount', random.randint(150, 400)),
                    'published_date': volume_info.get('publishedDate', '2020')
                }
                
                for identifier in volume_info.get('industryIdentifiers', []):
                    if identifier.get('type') in ['ISBN_13', 'ISBN_10']:
                        book_data['isbn'] = identifier.get('identifier')
                        break
                
                books_data.append(book_data)
    
    except Exception as e:
        print(f"Error searching for {category_name}: {e}")
    
    return books_data

def create_fallback_books(category_name):
    fallback_data = {
        'Fiction': [
            {'title': 'The Little Prince', 'author': 'Antoine de Saint-Exupéry', 'desc': 'A poetic and philosophical tale.', 'img': 'https://covers.openlibrary.org/b/isbn/9782070408504-M.jpg'},
            {'title': 'The Stranger', 'author': 'Albert Camus', 'desc': 'A major existentialist novel.', 'img': 'https://covers.openlibrary.org/b/isbn/9782070360024-M.jpg'},
            {'title': 'Madame Bovary', 'author': 'Gustave Flaubert', 'desc': 'A classic of French literature.', 'img': 'https://covers.openlibrary.org/b/isbn/9782070413119-M.jpg'},
            {'title': 'Les Misérables', 'author': 'Victor Hugo', 'desc': 'A social epic of 19th century France.', 'img': 'https://covers.openlibrary.org/b/isbn/9782070409228-M.jpg'},
            {'title': 'The Red and the Black', 'author': 'Stendhal', 'desc': 'An essential coming-of-age novel.', 'img': 'https://covers.openlibrary.org/b/isbn/9782070413080-M.jpg'}
        ],
        'Science Fiction': [
            {'title': 'Dune', 'author': 'Frank Herbert', 'desc': 'A legendary space epic.', 'img': 'https://covers.openlibrary.org/b/isbn/9780441172719-M.jpg'},
            {'title': '1984', 'author': 'George Orwell', 'desc': 'A prophetic dystopia.', 'img': 'https://covers.openlibrary.org/b/isbn/9780451524935-M.jpg'},
            {'title': 'Foundation', 'author': 'Isaac Asimov', 'desc': 'The Foundation cycle.', 'img': 'https://covers.openlibrary.org/b/isbn/9780553293357-M.jpg'},
            {'title': 'Neuromancer', 'author': 'William Gibson', 'desc': 'The founding novel of cyberpunk.', 'img': 'https://covers.openlibrary.org/b/isbn/9780441569595-M.jpg'},
            {'title': 'The Time Machine', 'author': 'H.G. Wells', 'desc': 'A science fiction classic.', 'img': 'https://covers.openlibrary.org/b/isbn/9780486284729-M.jpg'}
        ],
        'Fantasy': [
            {'title': 'The Lord of the Rings', 'author': 'J.R.R. Tolkien', 'desc': 'The ultimate fantasy epic.', 'img': 'https://covers.openlibrary.org/b/isbn/9780547928227-M.jpg'},
            {'title': 'Harry Potter and the Sorcerer\'s Stone', 'author': 'J.K. Rowling', 'desc': 'The beginning of the magical saga.', 'img': 'https://covers.openlibrary.org/b/isbn/9780439708180-M.jpg'},
            {'title': 'A Game of Thrones', 'author': 'George R.R. Martin', 'desc': 'An epic fantasy saga.', 'img': 'https://covers.openlibrary.org/b/isbn/9780553103540-M.jpg'},
            {'title': 'Eragon', 'author': 'Christopher Paolini', 'desc': 'The story of a Dragon Rider.', 'img': 'https://covers.openlibrary.org/b/isbn/9780375826696-M.jpg'},
            {'title': 'The Chronicles of Narnia', 'author': 'C.S. Lewis', 'desc': 'A magical world to discover.', 'img': 'https://covers.openlibrary.org/b/isbn/9780064404990-M.jpg'}
        ],
        'Mystery': [
            {'title': 'Murder on the Orient Express', 'author': 'Agatha Christie', 'desc': 'A Hercule Poirot investigation.', 'img': 'https://covers.openlibrary.org/b/isbn/9780062693662-M.jpg'},
            {'title': 'Maigret Sets a Trap', 'author': 'Georges Simenon', 'desc': 'An Inspector Maigret investigation.', 'img': 'https://covers.openlibrary.org/b/isbn/9782253142225-M.jpg'},
            {'title': 'The Maltese Falcon', 'author': 'Dashiell Hammett', 'desc': 'A noir classic.', 'img': 'https://covers.openlibrary.org/b/isbn/9780679722649-M.jpg'},
            {'title': 'The Murder at the Vicarage', 'author': 'Agatha Christie', 'desc': 'Miss Marple\'s first investigation.', 'img': 'https://covers.openlibrary.org/b/isbn/9780062073570-M.jpg'},
            {'title': 'The Mousetrap', 'author': 'Agatha Christie', 'desc': 'A mysterious locked-room mystery.', 'img': 'https://covers.openlibrary.org/b/isbn/9780573010101-M.jpg'}
        ],
        'Biography': [
            {'title': 'Steve Jobs', 'author': 'Walter Isaacson', 'desc': 'The biography of Apple\'s founder.', 'img': 'https://covers.openlibrary.org/b/isbn/9781451648539-M.jpg'},
            {'title': 'Gandhi', 'author': 'Louis Fischer', 'desc': 'The life of Mahatma Gandhi.', 'img': 'https://covers.openlibrary.org/b/isbn/9780451627742-M.jpg'},
            {'title': 'Einstein', 'author': 'Walter Isaacson', 'desc': 'The life of the physics genius.', 'img': 'https://covers.openlibrary.org/b/isbn/9780743264747-M.jpg'},
            {'title': 'Churchill', 'author': 'Andrew Roberts', 'desc': 'Biography of the British Prime Minister.', 'img': 'https://covers.openlibrary.org/b/isbn/9780670026203-M.jpg'},
            {'title': 'Marie Curie', 'author': 'Ève Curie', 'desc': 'The life of the first female Nobel laureate.', 'img': 'https://covers.openlibrary.org/b/isbn/9780306810381-M.jpg'}
        ],
        'Self Help': [
            {'title': 'The 7 Habits of Highly Effective People', 'author': 'Stephen Covey', 'desc': 'Guide to personal effectiveness.', 'img': 'https://covers.openlibrary.org/b/isbn/9781982137274-M.jpg'},
            {'title': 'How to Win Friends and Influence People', 'author': 'Dale Carnegie', 'desc': 'The art of human relations.', 'img': 'https://covers.openlibrary.org/b/isbn/9780671027032-M.jpg'},
            {'title': 'Think and Grow Rich', 'author': 'Napoleon Hill', 'desc': 'Keys to financial success.', 'img': 'https://covers.openlibrary.org/b/isbn/9781585424337-M.jpg'},
            {'title': 'The Power of Now', 'author': 'Eckhart Tolle', 'desc': 'Spiritual guide for transformation.', 'img': 'https://covers.openlibrary.org/b/isbn/9781577314806-M.jpg'},
            {'title': 'Rich Dad Poor Dad', 'author': 'Robert Kiyosaki', 'desc': 'Financial education for everyone.', 'img': 'https://covers.openlibrary.org/b/isbn/9781612680194-M.jpg'}
        ]
    }
    
    books_data = []
    for book_info in fallback_data.get(category_name, []):
        books_data.append({
            'title': book_info['title'],
            'authors': [book_info['author']],
            'description': book_info['desc'],
            'isbn': None,
            'thumbnail': book_info['img'],
            'page_count': random.randint(200, 400),
            'published_date': '2020'
        })
    
    return books_data

def download_image(url):
    if not url:
        return None
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        print(f"Downloading image: {url}")
        response = requests.get(url, timeout=20, headers=headers, stream=True)
        if response.status_code == 200 and len(response.content) > 500:
            print(f"Image downloaded successfully ({len(response.content)} bytes)")
            return ContentFile(response.content)
        else:
            print(f"Download failed: status {response.status_code}, size {len(response.content)}")
    except Exception as e:
        print(f"Error downloading image {url}: {e}")
    
    return None

def create_categories():
    categories_data = [
        {
            'name': 'Fiction',
            'description': 'Narrative prose works of fiction'
        },
        {
            'name': 'Science Fiction',
            'description': 'Books exploring scientific concepts and futures'
        },
        {
            'name': 'Fantasy',
            'description': 'Works incorporating magical and supernatural elements'
        },
        {
            'name': 'Mystery',
            'description': 'Novels featuring criminal investigations'
        },
        {
            'name': 'Biography',
            'description': 'Stories of real people\'s lives'
        },
        {
            'name': 'Self Help',
            'description': 'Books to improve personal and professional life'
        }
    ]
    
    categories = {}
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        categories[cat_data['name']] = category
        print(f"Category {'created' if created else 'exists'}: {cat_data['name']}")
    
    return categories

def create_authors(author_names):
    authors = {}
    for author_name in author_names:
        author, created = Author.objects.get_or_create(name=author_name)
        authors[author_name] = author
        if created:
            print(f"Author created: {author_name}")
    
    return authors

def populate_database():
    print("Starting database population...")
    
    categories = create_categories()
    
    all_books_created = 0
    
    for category_name, category_obj in categories.items():
        print(f"\nSearching books for category: {category_name}")
        
        books_data = search_books_by_category(category_name, max_results=8)
        
        if not books_data:
            print(f"API returns nothing for {category_name}, creating fictional books...")
            books_data = create_fallback_books(category_name)
            
        books_created = 0
        author_names = set()
        
        for book_data in books_data:
            author_names.update(book_data['authors'])
        
        authors = create_authors(author_names)
        
        for book_data in books_data:
            existing_book = Book.objects.filter(title=book_data['title']).first()
            if existing_book:
                continue
            
            try:
                author_name = book_data['authors'][0]
                author = authors.get(author_name)
                
                if not author:
                    continue
                
                isbn = book_data['isbn']
                if not isbn:
                    isbn = f"9{random.randint(100000000000, 999999999999)}"
                
                price = round(random.uniform(800, 3500), 2)
                stock_quantity = random.randint(5, 50)
                book = Book(
                    title=book_data['title'][:200],
                    author=author,
                    category=category_obj,
                    isbn=isbn[:13],
                    description=book_data['description'][:1000] if book_data['description'] else "Description not available.",
                    price=price,
                    stock_quantity=stock_quantity
                )
                
                image_saved = False
                if book_data['thumbnail']:
                    thumbnail_url = book_data['thumbnail'].replace('http://', 'https://')
                    image_file = download_image(thumbnail_url)
                    if image_file:
                        filename = f"{isbn}_{category_name.replace(' ', '_').replace('-', '_')}.jpg"
                        book.cover_image.save(filename, image_file, save=False)
                        image_saved = True
                
                book.save()
                books_created += 1
                all_books_created += 1
                
                image_status = "with image" if image_saved else "without image"
                print(f"✓ Book created ({image_status}): {book_data['title'][:40]}... - {author_name}")
                
                if books_created >= 5:
                    break
                    
            except Exception as e:
                print(f"✗ Error creating book {book_data['title']}: {e}")
                continue
    
    print(f"\nPopulation complete! {all_books_created} books created in total.")
    
    print("\nSummary by category:")
    for category_name, category_obj in categories.items():
        count = Book.objects.filter(category=category_obj).count()
        print(f"  {category_name}: {count} books")

if __name__ == "__main__":
    populate_database()