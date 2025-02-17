"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
import user.urls, closet.urls
from closet.views import dashboard_view, custom_500_error
from django.conf import settings
from django.conf.urls.static import static
# 404 페이지
from django.shortcuts import render
from user.views import robots_txt, index_view
from django.contrib.sitemaps.views import sitemap
from config.sitemaps import sitemaps  # config/sitemaps.py에서 import
from django.views.generic import RedirectView


def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index'),
    path('', include(('closet.urls', 'closet'), namespace='closet')),
    path('' , include('user.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('accounts/', include('allauth.urls')),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    # favicon.ico 요청을 static 파일로 리다이렉트
    re_path(r'^favicon\.ico$', RedirectView.as_view(
        url='/static/images/favicon/favicon.ico', permanent=True)),
]

handler404 = custom_404
handler500 = custom_500


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]