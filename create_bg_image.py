from PIL import Image, ImageDraw, ImageFont
import os

width, height = 1920, 1080
img = Image.new('RGB', (width, height), (45, 55, 72))

for y in range(height):
    ratio = y / height
    r = int(45 * (1 - ratio) + 74 * ratio)
    g = int(55 * (1 - ratio) + 85 * ratio)
    b = int(72 * (1 - ratio) + 104 * ratio)
    
    for x in range(width):
        variation = (x + y) % 50
        r_var = min(255, max(0, r + variation // 10))
        g_var = min(255, max(0, g + variation // 10))
        b_var = min(255, max(0, b + variation // 10))
        img.putpixel((x, y), (r_var, g_var, b_var))

draw = ImageDraw.Draw(img)

overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
overlay_draw = ImageDraw.Draw(overlay)

circles = [
    (200, 200, 150, (255, 255, 255, 20)),
    (1600, 300, 200, (255, 255, 255, 15)),
    (800, 700, 180, (255, 255, 255, 25)),
    (1400, 800, 120, (255, 255, 255, 18))
]

for x, y, radius, color in circles:
    overlay_draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=color)

img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')

bg_path = os.path.join('media', 'images', 'bg.jpg')
os.makedirs(os.path.dirname(bg_path), exist_ok=True)
img.save(bg_path, 'JPEG', quality=95)
print(f"Image de fond créée: {bg_path}")