

# Create your models here.

from django.db import models

class Outfit(models.Model):
    DESIGN_STYLE_CHOICES = [
        ('Street', 'Street'),
        ('Casual', 'Casual'),
        ('Formal', 'Formal'),
    ]

    CATEGORY_CHOICES = [
        ('T-shirt', 'T-shirt'),
        ('Blouse', 'Blouse'),
        ('Pants', 'Pants'),
        ('Dress', 'Dress'),
        ('Skirt', 'Skirt'),
        ('Jacket', 'Jacket'),
        ('Coat', 'Coat'),
    ]

    design_style = models.CharField(max_length=50, choices=DESIGN_STYLE_CHOICES, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True)
    overall_design = models.TextField(blank=True)
    logo_location = models.CharField(max_length=100, blank=True)
    logo_size = models.CharField(max_length=100, blank=True)
    logo_content = models.TextField(blank=True)
    color_and_pattern = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=100, blank=True)
    fit = models.CharField(max_length=50, blank=True)
    cloth_length = models.CharField(max_length=50, blank=True)
    neckline = models.CharField(max_length=50, blank=True)
    detail = models.TextField(blank=True)
    material = models.CharField(max_length=100, blank=True)
    season = models.CharField(max_length=50, blank=True)
    tag = models.JSONField(blank=True, default=list)
    comment = models.TextField(blank=True)
    brand = models.CharField(max_length=100, blank=True)
    price = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='outfits/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image_url = models.CharField(max_length=300, blank=True)
    def __str__(self):
        return f"{self.category} - {self.design_style}"
