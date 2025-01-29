from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings


def dashboard_view(request):
    user = request.user  # 현재 로그인한 사용자
    username = user.username  # OAuth 연결 여부와 상관없이 사용자 이름을 사용
    return render(request, 'closet/dashboard.html', {'username': username})

@login_required
def closet_start_view(request):
    return render(request, 'closet_start.html')

@login_required
def closet_history_view(request):
    return render(request, 'closet_history.html')



def weather_view(request):
    return render(request, 'closet/weather.html',{
         'OPENWEATHER_API_KEY': settings.OPENWEATHER_API_KEY
    })



