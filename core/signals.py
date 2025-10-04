from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from . models import Order, User
import random
import string

@receiver(post_save, sender=Order)
def generate_order_number(sender, instance, created, **kwargs):
    if created and not instance.order_number:
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        instance.order_number = f"ORD-{random_str}"
        instance.save()