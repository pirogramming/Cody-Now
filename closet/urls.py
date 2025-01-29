#urls.py
from django.urls import path
from closet import views
from .views import dashboard_view, closet_start_view, closet_history_view, weather_view
app_name = 'closet'

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),

    path('weather/', weather_view, name='weather'),
    
    path('upload/', views.upload_outfit, name='upload_outfit'),
]


