from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from closet.models import Outfit, ClothingItem  # 옷장 관련 모델 추가

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "daily"
    protocol = "https"

    def items(self):
        return [
            'home',             # 메인 페이지
            'user:login',       # 로그인
            'user:signup',      # 회원가입
            'closet:dashboard'  # 대시보드
        ]

    def location(self, item):
        return reverse(item)

class OutfitSitemap(Sitemap):
    priority = 0.7
    changefreq = "daily"
    protocol = "https"

    def items(self):
        return Outfit.objects.filter(is_public=True)  # 공개된 코디만 포함

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('closet:outfit_detail', args=[obj.id])

class ClothingItemSitemap(Sitemap):
    priority = 0.6
    changefreq = "weekly"
    protocol = "https"

    def items(self):
        return ClothingItem.objects.filter(is_public=True)  # 공개된 의류 아이템만 포함

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('closet:clothing_detail', args=[obj.id])

# urls.py에서 사용할 sitemaps 딕셔너리
sitemaps = {
    'static': StaticViewSitemap,
    'outfits': OutfitSitemap,
    'clothing': ClothingItemSitemap,
}
