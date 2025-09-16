import uuid
from django.db import models

# Create your models here.

class Product(models.Model):

    CATEGORY_CHOICES = [
        ('misc', 'Lain-Lain')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField(default=0)
    description = models.TextField()
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, default='misc')
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name
