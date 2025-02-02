#urls.py
from django.urls import path
from closet import views
from .views import evaluate_closet


app_name = 'closet'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('weather/', views.weather_view, name='weather'),
    path('api/weather/', views.get_weather_data, name='get_weather_data'),
    path('upload/', views.upload_outfit, name='upload_outfit'),
    path('gen-cody/', views.gen_cody, name='gen_cody'),
    path('post-analysis/', views.post_analysis, name='post_analysis'),  # 분석 결과 저장용 URL
    path("add-category/", views.add_category, name="add_category"),
    path("delete-category/", views.delete_category, name="delete_category"),
    # path('evaluate_closet/', evaluate_closet, name='evaluate_closet'),

    path('evaluate_closet/', evaluate_closet, name='evaluate_closet'),

   
]


