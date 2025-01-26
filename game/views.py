from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def dashboard_view(request):
    user = request.user  # 현재 로그인한 사용자
    username = user.username  # OAuth 연결 여부와 상관없이 사용자 이름을 사용
    return render(request, 'game/dashboard.html', {'username': username})

@login_required
def game_start_view(request):
    return render(request, 'game_start.html')

@login_required
def game_history_view(request):
    return render(request, 'game_history.html')
