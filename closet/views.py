from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


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


#기능 6번
import google.generativeai as genai
import os
from dotenv import load_dotenv

def generate():
    # .env 파일에서 API 키 로드
    load_dotenv()
    GEN_CODY_API_KEY = os.getenv('INPUT_API_KEY')
    
    # API 키 설정
    genai.configure(api_key=GEN_CODY_API_KEY)
    
    # 모델 설정
    model = genai.GenerativeModel('gemini-pro')
    
    # 프롬프트 생성 및 응답 받기
    prompt = "기온이 20도정도 되는 날씨의 옷을 추천해줘"
    response = model.generate_content(prompt)
    
    print(response.text)

generate()