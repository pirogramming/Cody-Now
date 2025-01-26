#urls.py
from django.urls import path
from game import views
from .views import dashboard_view, game_start_view, game_history_view
app_name = 'game'

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
]