# Create your models here.

from django.db import models
from django.conf import settings

class UserCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

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

    # 사용자 정보 추가
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='outfits',
        null=True  # null 허용
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 이미지 정보
    image = models.ImageField(upload_to='outfits/', blank=True, null=True)
    image_url = models.CharField(max_length=300, blank=True)
    

       # 사용자가 추가한 카테고리 (ex. 여름옷, 겨울옷)
    user_category = models.ForeignKey(UserCategory, on_delete=models.SET_NULL, null=True, blank=True)


    # Gemini API 분석 결과
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

    # Gemini API 원본 응답 저장
    raw_response = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - {self.category} ({self.created_at})"
