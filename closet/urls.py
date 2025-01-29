#urls.py
from django.urls import path
from closet import views
from .views import dashboard_view, closet_start_view, closet_history_view
app_name = 'closet'

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('generate/', views.generate, name='generate'),
    path('output/', views.generate, name='output'),  # generate 함수와 연결
]