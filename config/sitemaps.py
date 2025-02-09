from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from closet.models import Outfit

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "daily"
    protocol = "https"

    def items(self):
        return [
            'index',                   # 'home'을 'index'로 변경
            'user:login',             # 로그인
            'user:signup',            # 회원가입
            'closet:dashboard',       # 대시보드
            'closet:weather',         # 날씨
            'closet:upload_outfit',   # 옷 업로드
            'closet:gen_cody',        # 코디 생성
            'closet:closet_main',     # 옷장 메인
            'closet:upload_history',  # 업로드 히스토리
            'closet:evaluate_closet', # 옷장 평가
        ]

    def location(self, item):
        return reverse(item)

class OutfitSitemap(Sitemap):
    priority = 0.7
    changefreq = "daily"
    protocol = "https"

    def items(self):
        return Outfit.objects.filter(wearable=True).order_by('-created_at')

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        # outfit_detail URL이 없으므로 upload_history로 연결
        return reverse('closet:upload_history')

# urls.py에서 사용할 sitemaps 딕셔너리
sitemaps = {
    'static': StaticViewSitemap,
    'outfits': OutfitSitemap,
}
