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
from django.urls import path, include
import user.urls, closet.urls
from closet.views import dashboard_view, custom_500_error
from django.conf import settings
from django.conf.urls.static import static
# 404 페이지
from django.shortcuts import render

def your_404(request, exception):
    return render(request, '404.html', status=404)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard_view, name='home'),
    path('', include(closet.urls)),
    path('' , include(user.urls)),
    path('', include('social_django.urls', namespace='social')),
    path('accounts/', include('allauth.urls')),
    
]

handler404 = your_404


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]

handler500 = 'closet.views.custom_500_error'