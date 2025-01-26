from django.urls import path, include 
from django.contrib.auth.views import LogoutView
from user import views

app_name="user"

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('auth/', include('social_django.urls', namespace='social')),
]