#urls.py
from django.urls import path
from closet import views
from .views import dashboard_view, closet_start_view, closet_history_view
app_name = 'closet'

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('upload/', views.upload_outfit, name='upload_outfit'),
    path('post_input/', views.post_input, name='post_input'), #은경아 이거 수정해야돼

]


