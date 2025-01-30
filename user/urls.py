from django.urls import path, include 
from user import views
from django.contrib.auth import views as auth_views

from .views import user_profile_view, edit_profile_view
from .views import CustomPasswordResetView, CustomPasswordResetConfirmView

app_name="user"

urlpatterns = [
    path('user/login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('auth/', include('social_django.urls', namespace='social')),

    path("profile/", user_profile_view, name="user_profile"),
    path("edit-profile/", edit_profile_view, name="edit_profile"),

    path("password-reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path("password-reset-confirm/<uidb64>/<token>/", CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]