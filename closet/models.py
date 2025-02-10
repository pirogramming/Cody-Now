# Create your models here.

from django.db import models
from django.conf import settings
import django.db.models.deletion  # 명시적으로 import 추가

# 1. 기본 모델들
class UserCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=django.db.models.deletion.CASCADE,  # 전체 경로 지정
        related_name='category',
        null=True
    )

    def __str__(self):
        return f"{self.name}"

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
    # 나의 옷장에서 사용
    bookmarked = models.BooleanField(default=False)
    #의류임 판명
    wearable=models.BooleanField(default=False)
    # Gemini API 원본 응답 저장
    raw_response = models.JSONField(blank=True, null=True)

    #유저카테고리 받아오기
    usercategories = models.ManyToManyField(UserCategory, related_name='outfits', blank=True)


    def __str__(self):
        return f"{self.user.email} - {self.category} ({self.created_at})"

class RecommendationResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE)
    outfit = models.ForeignKey(
        'Outfit', 
        on_delete=django.db.models.deletion.SET_NULL,  # 전체 경로 지정
        null=True, 
        blank=True, 
        related_name='recommendations'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    original_text = models.TextField(help_text="Gemini API가 생성한 원본 마크다운 텍스트")
    html_content = models.TextField(help_text="변환된 HTML 컨텐츠")

    def __str__(self):
        return f"Recommendation for {self.user.email} at {self.created_at}"

# 2. 관계 모델들
class RecommendedProduct(models.Model):
    recommendation = models.ForeignKey(RecommendationResult, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    image_url = models.URLField()
    purchase_url = models.URLField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.created_at}"

class MyCloset(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='my_closet',
        null=True
    )
    outfit = models.ForeignKey(
        'Outfit',  # 문자열로 참조하여 순환 참조 방지
        on_delete=models.CASCADE
    )
    user_category = models.ForeignKey(
        'UserCategory',  # 문자열로 참조하여 순환 참조 방지
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)


class AnalysisResult(models.Model):  # 🔹 AI 분석 결과를 저장하는 모델
    outfit = models.OneToOneField(Outfit, on_delete=models.CASCADE, related_name="analysis_result")
    result_text = models.TextField()  # AI 분석 결과
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AnalysisResult for {self.outfit.id}"