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
    # path('evaluate_closet/', evaluate_closet, name='evaluate_closet'),

    path('evaluate_closet/', evaluate_closet, name='evaluate_closet'),
<<<<<<< HEAD

    path('closet_main/', views.closet_main, name='closet_main'),
    path('bookmark/<int:outfit_id>/', views.toggle_bookmark, name='toggle_bookmark'),
    path('delete/<int:outfit_id>/', views.delete_outfit, name='delete_outfit'),
=======
    #path('evaluate_closet/', views.recommend_item, name='recommend_item'), #기본템 추천
>>>>>>> 2831e72524b8174106e85402d0c23684206697ec
]


