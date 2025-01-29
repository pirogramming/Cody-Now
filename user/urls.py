from django.urls import path, include 
from user import views
from django.contrib.auth import views as auth_views

from .views import user_profile_view

app_name="user"

urlpatterns = [
    path('user/login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('auth/', include('social_django.urls', namespace='social')),

    path("profile/", user_profile_view, name="user_profile"),
]