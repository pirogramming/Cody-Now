from django.urls import path, include 
from user import views
from django.contrib.auth import views as auth_views
from .sitemaps import StaticViewSitemap, OutfitSitemap, ClothingItemSitemap
from .views import user_profile_view, edit_profile_view, view_profile_view
from django.contrib.sitemaps.views import sitemap

app_name = "user"


sitemaps = {
    'static': StaticViewSitemap,
    'outfits': OutfitSitemap,
    'clothing': ClothingItemSitemap,
}

urlpatterns = [
    path('user/login/', views.login_view, name='login'),

    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('auth/', include('social_django.urls', namespace='social')),

    path("profile/", user_profile_view, name="user_profile"),
    path("view-profile/", view_profile_view, name="view_profile"),
    path("edit-profile/", edit_profile_view, name="edit_profile"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
]