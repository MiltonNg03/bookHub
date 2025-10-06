import os
import sys
import django
import requests
from django.core.files.base import ContentFile
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import textwrap

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BookHub.settings')
django.setup()

from core.models import Category, Author, Book
import random

def search_books_by_category(category_name, max_results=10):
    return []

def create_fallback_books(category_name):
    fallback_data = {
        'Literature': [
            {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'desc': 'A classic American novel.'},
            {'title': '1984', 'author': 'George Orwell', 'desc': 'Dystopian social science fiction.'},
            {'title': 'Pride and Prejudice', 'author': 'Jane Austen', 'desc': 'Romantic fiction classic.'}
        ],
        'Educational / School Books': [
            {'title': 'Introduction to Algorithms', 'author': 'Thomas Cormen', 'desc': 'Comprehensive algorithms textbook.'},
            {'title': 'Calculus', 'author': 'James Stewart', 'desc': 'Mathematical analysis textbook.'},
            {'title': 'Physics Principles', 'author': 'David Halliday', 'desc': 'Fundamental physics concepts.'}
        ],
        'Science and Technology': [
            {'title': 'A Brief History of Time', 'author': 'Stephen Hawking', 'desc': 'Cosmology for general readers.'},
            {'title': 'The Innovators', 'author': 'Walter Isaacson', 'desc': 'Digital revolution history.'},
            {'title': 'Sapiens', 'author': 'Yuval Noah Harari', 'desc': 'Brief history of humankind.'}
        ],
        'Human and Social Sciences': [
            {'title': 'Thinking, Fast and Slow', 'author': 'Daniel Kahneman', 'desc': 'Behavioral psychology insights.'},
            {'title': 'The Social Animal', 'author': 'David Brooks', 'desc': 'Human nature and society.'},
            {'title': 'Guns, Germs, and Steel', 'author': 'Jared Diamond', 'desc': 'Societal development factors.'}
        ],
        'Economics and Management': [
            {'title': 'Good to Great', 'author': 'Jim Collins', 'desc': 'What makes companies excel.'},
            {'title': 'The Lean Startup', 'author': 'Eric Ries', 'desc': 'Building successful businesses.'},
            {'title': 'Freakonomics', 'author': 'Steven Levitt', 'desc': 'Hidden side of everything.'}
        ],
        'Languages': [
            {'title': 'English Grammar in Use', 'author': 'Raymond Murphy', 'desc': 'Essential English grammar.'},
            {'title': 'French for Beginners', 'author': 'Marie Dubois', 'desc': 'Learn French basics.'},
            {'title': 'Spanish Vocabulary', 'author': 'Carlos Martinez', 'desc': 'Essential Spanish words.'}
        ],
        'Personal Development': [
            {'title': 'The 7 Habits of Highly Effective People', 'author': 'Stephen Covey', 'desc': 'Guide to personal effectiveness.'},
            {'title': 'Atomic Habits', 'author': 'James Clear', 'desc': 'Building good habits.'},
            {'title': 'Mindset', 'author': 'Carol Dweck', 'desc': 'The psychology of success.'}
        ],
        'Arts and Culture': [
            {'title': 'The Story of Art', 'author': 'Ernst Gombrich', 'desc': 'Comprehensive art history.'},
            {'title': 'Ways of Seeing', 'author': 'John Berger', 'desc': 'Art criticism and theory.'},
            {'title': 'The Power of Music', 'author': 'Elena Mannes', 'desc': 'Music and the brain.'}
        ],
        'Religion and Spirituality': [
            {'title': 'The Power of Now', 'author': 'Eckhart Tolle', 'desc': 'Spiritual awakening guide.'},
            {'title': 'Man\'s Search for Meaning', 'author': 'Viktor Frankl', 'desc': 'Finding purpose in life.'},
            {'title': 'The Alchemist', 'author': 'Paulo Coelho', 'desc': 'Spiritual journey novel.'}
        ],
        'Leisure and Practical Life': [
            {'title': 'The Joy of Cooking', 'author': 'Irma Rombauer', 'desc': 'Classic cookbook.'},
            {'title': 'Home Improvement Guide', 'author': 'Bob Vila', 'desc': 'DIY home projects.'},
            {'title': 'Gardening Basics', 'author': 'Sarah Green', 'desc': 'Essential gardening tips.'}
        ],
        'Health / Well-being': [
            {'title': 'The Blue Zones', 'author': 'Dan Buettner', 'desc': 'Secrets of longevity.'},
            {'title': 'Why We Sleep', 'author': 'Matthew Walker', 'desc': 'The power of sleep.'},
            {'title': 'Mindfulness', 'author': 'Ellen Langer', 'desc': 'The psychology of possibility.'}
        ],
        'Sustainable Development / Ecology': [
            {'title': 'Silent Spring', 'author': 'Rachel Carson', 'desc': 'Environmental conservation classic.'},
            {'title': 'The Sixth Extinction', 'author': 'Elizabeth Kolbert', 'desc': 'Mass extinction events.'},
            {'title': 'Cradle to Cradle', 'author': 'Michael Braungart', 'desc': 'Sustainable design principles.'}
        ],
        'Biographies and Testimonies': [
            {'title': 'Steve Jobs', 'author': 'Walter Isaacson', 'desc': 'The biography of Apple\'s founder.'},
            {'title': 'Becoming', 'author': 'Michelle Obama', 'desc': 'Former First Lady\'s memoir.'},
            {'title': 'Long Walk to Freedom', 'author': 'Nelson Mandela', 'desc': 'Autobiography of the freedom fighter.'}
        ],
        'Law': [
            {'title': 'Constitutional Law', 'author': 'Geoffrey Stone', 'desc': 'Fundamental legal principles.'},
            {'title': 'Criminal Justice', 'author': 'Frank Schmalleger', 'desc': 'Criminal law overview.'},
            {'title': 'Contract Law', 'author': 'Steven Burton', 'desc': 'Legal agreements guide.'}
        ],
        'Methodology / Research': [
            {'title': 'Research Methods', 'author': 'John Creswell', 'desc': 'Qualitative and quantitative research.'},
            {'title': 'The Craft of Research', 'author': 'Wayne Booth', 'desc': 'Academic writing guide.'},
            {'title': 'Statistics for Researchers', 'author': 'David Moore', 'desc': 'Statistical analysis methods.'}
        ]
    }
    
    books_data = []
    for book_info in fallback_data.get(category_name, []):
        books_data.append({
            'title': book_info['title'],
            'authors': [book_info['author']],
            'description': book_info['desc'],
            'isbn': None,
            'thumbnail': None,
            'page_count': random.randint(200, 400),
            'published_date': '2020'
        })
    
    return books_data

def create_book_cover(title, author, category_name, isbn):
    color_schemes = {
        'Literature': (139, 69, 19),
        'Educational / School Books': (0, 100, 0),
        'Science and Technology': (70, 130, 180),
        'Human and Social Sciences': (128, 0, 128),
        'Economics and Management': (184, 134, 11),
        'Languages': (220, 20, 60),
        'Personal Development': (255, 140, 0),
        'Arts and Culture': (75, 0, 130),
        'Religion and Spirituality': (25, 25, 112),
        'Leisure and Practical Life': (34, 139, 34),
        'Health / Well-being': (0, 128, 128),
        'Sustainable Development / Ecology': (107, 142, 35),
        'Biographies and Testimonies': (139, 0, 0),
        'Law': (72, 61, 139),
        'Methodology / Research': (105, 105, 105)
    }
    
    base_color = color_schemes.get(category_name, (70, 130, 180))
    width, height = 300, 450
    
    img = Image.new('RGB', (width, height), base_color)
    draw = ImageDraw.Draw(img)
    
    for y in range(height):
        for x in range(width):
            noise = random.randint(-15, 15)
            r = max(0, min(255, base_color[0] + noise))
            g = max(0, min(255, base_color[1] + noise))
            b = max(0, min(255, base_color[2] + noise))
            img.putpixel((x, y), (r, g, b))
    
    draw = ImageDraw.Draw(img)
    
    border_color = tuple(max(0, c - 40) for c in base_color)
    draw.rectangle([10, 10, width-10, height-10], outline=border_color, width=3)
    draw.rectangle([15, 15, width-15, height-15], outline=border_color, width=1)
    
    try:
        title_font = ImageFont.truetype("arial.ttf", 24)
        author_font = ImageFont.truetype("arial.ttf", 16)
        small_font = ImageFont.truetype("arial.ttf", 12)
    except:
        title_font = ImageFont.load_default()
        author_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    title_area_y = 40
    title_lines = textwrap.wrap(title, width=20)
    
    for line in title_lines:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        
        draw.text((x + 1, title_area_y + 1), line, fill=(0, 0, 0), font=title_font)
        draw.text((x, title_area_y), line, fill=(255, 255, 255), font=title_font)
        title_area_y += 30
    
    line_y = title_area_y + 20
    draw.line([(50, line_y), (width-50, line_y)], fill=(255, 255, 255), width=2)
    
    center_y = height // 2
    pattern_color = tuple(min(255, c + 30) for c in base_color)
    
    diamond_size = 40
    center_x = width // 2
    diamond_points = [
        (center_x, center_y - diamond_size),
        (center_x + diamond_size, center_y),
        (center_x, center_y + diamond_size),
        (center_x - diamond_size, center_y)
    ]
    draw.polygon(diamond_points, fill=pattern_color, outline=(255, 255, 255), width=2)
    
    author_y = height - 80
    author_lines = textwrap.wrap(author, width=25)
    
    for line in author_lines:
        bbox = draw.textbbox((0, 0), line, font=author_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        
        draw.text((x + 1, author_y + 1), line, fill=(0, 0, 0), font=author_font)
        draw.text((x, author_y), line, fill=(255, 255, 255), font=author_font)
        author_y += 20
    
    isbn_text = f"ISBN: {isbn[:13]}"
    draw.text((width - 120, height - 25), isbn_text, fill=(200, 200, 200), font=small_font)
    
    filename = f"{isbn}_{category_name.replace(' ', '_').replace('/', '_')}.jpg"
    cover_path = os.path.join(project_root, 'media', 'book_covers', filename)
    os.makedirs(os.path.dirname(cover_path), exist_ok=True)
    img.save(cover_path, 'JPEG', quality=95)
    
    return f"book_covers/{filename}"

def create_categories():
    categories_data = [
        {'name': 'Literature', 'description': 'Classic and contemporary literary works'},
        {'name': 'Educational / School Books', 'description': 'Textbooks and educational materials'},
        {'name': 'Science and Technology', 'description': 'Scientific research and technological advances'},
        {'name': 'Human and Social Sciences', 'description': 'Psychology, sociology, anthropology'},
        {'name': 'Economics and Management', 'description': 'Business, finance, and management'},
        {'name': 'Languages', 'description': 'Language learning and linguistics'},
        {'name': 'Personal Development', 'description': 'Self-improvement and life skills'},
        {'name': 'Arts and Culture', 'description': 'Art, music, theater, and cultural studies'},
        {'name': 'Religion and Spirituality', 'description': 'Religious texts and spiritual guidance'},
        {'name': 'Leisure and Practical Life', 'description': 'Hobbies, crafts, and practical guides'},
        {'name': 'Health / Well-being', 'description': 'Health, fitness, and wellness'},
        {'name': 'Sustainable Development / Ecology', 'description': 'Environmental and sustainability topics'},
        {'name': 'Biographies and Testimonies', 'description': 'Life stories and personal accounts'},
        {'name': 'Law', 'description': 'Legal texts and jurisprudence'},
        {'name': 'Methodology / Research', 'description': 'Research methods and academic writing'}
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
        print(f"\nCreating books for category: {category_name}")
        
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
                
                isbn = f"9{random.randint(100000000000, 999999999999)}"
                price = round(random.uniform(800, 3500), 2)
                stock_quantity = random.randint(5, 50)
                
                book = Book(
                    title=book_data['title'][:200],
                    author=author,
                    category=category_obj,
                    isbn=isbn[:13],
                    description=book_data['description'][:1000],
                    price=price,
                    stock_quantity=stock_quantity
                )
                
                cover_path = create_book_cover(book_data['title'], author_name, category_name, isbn)
                if cover_path:
                    book.cover_image = cover_path
                
                book.save()
                books_created += 1
                all_books_created += 1
                
                print(f"Book created: {book_data['title'][:40]}... - {author_name}")
                    
            except Exception as e:
                print(f"Error creating book {book_data['title']}: {e}")
                continue
    
    print(f"\nPopulation complete! {all_books_created} books created in total.")
    
    print("\nSummary by category:")
    for category_name, category_obj in categories.items():
        count = Book.objects.filter(category=category_obj).count()
        print(f"  {category_name}: {count} books")

if __name__ == "__main__":
    populate_database()