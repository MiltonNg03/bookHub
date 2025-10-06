from django import template
from django.utils.html import format_html
from django.templatetags.static import static

register = template.Library()

@register.simple_tag
def book_cover_with_text(book):
    """Génère une div avec l'image de couverture et le texte superposé"""
    if book.cover_image:
        cover_url = book.cover_image.url
    else:
        cover_url = static('covers/Blue.png')
    
    return format_html(
        '''<div style="position: relative; display: inline-block; width: 100%; height: 300px;">
            <img src="{}" alt="{}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 8px;">
            <div style="position: absolute; top: 20px; left: 0; right: 0; text-align: center; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);">
                <div style="font-weight: bold; font-size: 1.2rem; margin-bottom: 10px; padding: 0 10px;">{}</div>
            </div>
            <div style="position: absolute; bottom: 20px; left: 0; right: 0; text-align: center; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);">
                <div style="font-size: 0.9rem; padding: 0 10px;">{}</div>
            </div>
        </div>''',
        cover_url,
        book.title,
        book.title,
        book.author.name
    )