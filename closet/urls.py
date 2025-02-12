#urls.py
from django.urls import path
from closet import views
from .views import evaluate_closet
from .views import test_image_upload_html


app_name = 'closet'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('weather/', views.weather_view, name='weather'),
    path('api/weather/', views.get_weather_data, name='get_weather_data'),
    path('upload/', views.upload_outfit, name='upload_outfit'),
    path("test-upload/", views.test_upload_outfit, name="test_upload_outfit"),
    path('gen-cody/', views.gen_cody, name='gen_cody'),
    path('post-analysis/', views.post_analysis, name='post_analysis'),  # 분석 결과 저장용 URL
    path('usercategory/',views.usercategory_view, name="usercategory_view"),
    path("add-category/", views.add_category, name="add_category"),
    path("delete-category/", views.delete_category, name="delete_category"),
    path("save_outfit_to_closet/", views.save_outfit_to_closet, name="save_outfit_to_closet"),
    # path('evaluate_closet/', evaluate_closet, name='evaluate_closet'),

    path('evaluate_closet/', evaluate_closet, name='evaluate_closet'),


    path('bookmark/<int:outfit_id>/', views.toggle_bookmark, name='toggle_bookmark'),
    path('delete-outfit/<int:outfit_id>/', views.delete_outfit, name='delete_outfit'),
    path('api/outfit/<int:outfit_id>/', views.get_outfit_data, name='get_outfit_data'), #페이지 연결
    # path('upload/<int:outfit_id>/', views.upload_outfit_view, name='upload_outfit'),
    path('upload-history/', views.upload_history, name="upload_history"),


    path('mycloset/', views.mycloset_view, name="mycloset_view"),
    path("mycloset/category/<int:category_id>/", views.category_detail_view, name="category_detail"),

    path('update-analysis/', views.update_analysis_result, name='update_analysis_result'),
]


