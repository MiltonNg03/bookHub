import os
import random
import textwrap
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings

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
    cover_path = os.path.join(settings.MEDIA_ROOT, 'book_covers', filename)
    os.makedirs(os.path.dirname(cover_path), exist_ok=True)
    img.save(cover_path, 'JPEG', quality=95)
    
    return f"book_covers/{filename}"