from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.utils.text import get_valid_filename

import os
import base64
import json
import requests
import logging
import tempfile

import google.generativeai as genai
from PIL import Image  # Pillow 라이브러리 추가

# 로거 설정
logger = logging.getLogger(__name__)

@login_required
def dashboard_view(request):
    user = request.user
    return render(request, "closet/dashboard.html", {"user": user})

@login_required
def closet_start_view(request):
    return render(request, 'closet_start.html')

@login_required
def closet_history_view(request):
    outfits = Outfit.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'closet_history.html', {'outfits': outfits})


def weather_view(request):
    return render(request, 'weather.html')

def get_weather_data(request):
    api_key = settings.OPENWEATHER_API_KEY
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    if not lat or not lon:
        return JsonResponse({'error': '위도와 경도를 제공해야 합니다.'}, status=400)

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=kr"
    
    try:
        response = requests.get(url)
        data = response.json()
        return JsonResponse(data)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    
#5번 섹션(input)
from django.http import JsonResponse
from .forms import OutfitForm
from closet.models import Outfit


# 이미지 업로드 및 분석 View
@csrf_exempt
@login_required
def upload_outfit(request):
    if request.method == 'POST':
        form = OutfitForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                outfit = Outfit(user=request.user)
                image = form.cleaned_data['image']
                outfit.image = image
                outfit.save()
                
                image_path = outfit.image.path
                with open(image_path, "rb") as img_file:
                    base64_image = base64.b64encode(img_file.read()).decode("utf-8")
                
                analysis_result = call_gemini_api(base64_image)
                outfit.raw_response = analysis_result
                
                if isinstance(analysis_result, dict):
                    for field in ['design_style', 'category', 'overall_design', 
                                'logo_location', 'logo_size', 'logo_content',
                                'color_and_pattern', 'color', 'fit', 'cloth_length',
                                'neckline', 'detail', 'material', 'season', 'tag',
                                'comment', 'brand', 'price']:
                        if field in analysis_result:
                            setattr(outfit, field, analysis_result[field])
                
                outfit.save()
                
                return JsonResponse({
                    "message": "Analysis completed",
                    "data": analysis_result
                })
            
            except Exception as e:
                logger.error(f"Error in upload_outfit: {str(e)}", exc_info=True)
                return JsonResponse({"error": str(e)}, status=500)
    else:
        form = OutfitForm()
    
    return render(request, 'closet/input.html', {'form': form})

@csrf_exempt
def post_analysis(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # 여기서 분석 결과를 저장하거나 처리
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Method not allowed"}, status=405)

def call_gemini_api(base64_image):
    api_key = "INPUT_API_KEY"  # API 키
    genai.configure(api_key=settings.INPUT_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-pro-001") 

    prompt = """주어진 이미지를 상세히 분석하여 아래 메타데이터를 JSON 형식으로 출력하세요.
    JSON 코드 블록(```json ... ```) 없이 순수 JSON 데이터만 출력하세요.
    옷의 주요 특징을 객관적으로 파악하며, 명확히 보이지 않는 정보는 '확인 불가' 또는 '추정'으로 기재하세요. 
    디자인 세부 사항, 색상, 핏, 소재, 태그 등을 고려해 상세히 기술하십시오. 분석의 목적은 의류 정보 텍스트화 및 추천 시스템 구축입니다.
    
    추출할 메타데이터:
    * 디자인 양식: (스트릿, 캐주얼, 포멀 중 선택)
    * 옷 분류: (예: 티셔츠, 블라우스, 바지, 원피스, 스커트, 재킷, 코트 등)
    * 전체적인 디자인: (2문장으로 요약)
    * 로고, 레터링: (위치, 크기, 내용 등)
    * 색상 / 패턴 유무: (단색, 스트라이프, 체크, 플라워 등)
    * 색상 조합: (예: 톤온톤, 대비색, 유사색 등)
    * 핏: (예: 슬림핏, 레귤러핏, 루즈핏, 오버핏 등)
    * 기장: (상의: 크롭, 기본, 롱 / 하의: 숏, 미디, 롱 / 원피스: 미니, 미디, 맥시 등)
    * 넥라인: (예: V넥, 라운드넥, U넥, 터틀넥, 보트넥 등)
    * 디테일: (예: 단추, 지퍼, 포켓, 레이스, 프릴, 주름, 셔링 등)
    * 소재: (예: 면, 폴리에스터, 울, 실크, 데님, 가죽 등 / 혼방인 경우 혼용률 추정)
    * 시즌: (SS, FW 또는 간절기)
    * 태그: (예: 휴양지룩, 데일리룩, 오피스룩, 데이트룩, 미니멀룩, 빈티지룩 등)
    * 종합평: (옷의 특징과 전반적인 느낌을 간략하게 서술)
    * 브랜드: (확인 가능한 경우)
    * 가격대: (확인 가능한 경우 / 고가, 중가, 저가 등으로 표기 가능)

    출력 양식(JSON)
    {
     "design_style": "", 
     "category": "", 
     "overall_design": "",
     "logo_or_lettering": {
     "logo_location": "", 
     "logo_size": "", 
     "logo_content": ""
     },
     "color_and_pattern": "", 
     "color": "", 
     "fit": "", 
     "cloth_length": "", 
     "neckline": "", 
     "detail": "", 
     "material": "", 
     "season": "", 
     "tag": ["", ""],
     "comment": "",
     "brand": "", 
     "price": ""
    }"""

    try:
        response = model.generate_content(
            contents=[
                {
                    "parts": [
                        {"text": prompt},  # ✅ 프롬프트
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",  # ✅ 이미지 형식 추가
                                "data": base64_image  # ✅ Base64 인코딩된 이미지
                            }
                        }
                    ]
                }
            ]
        )
        # ✅ 응답 데이터가 비어있는지 확인
        if not response or not response.text.strip():
            return {"error": "Gemini API에서 응답이 없습니다."}
        
        
        response_json = json.loads(response.text)
        return response_json  # JSON 응답 반환
    except json.JSONDecodeError as e:
        return {"error": f"JSON 변환 오류: {str(e)}", "raw_response": response.text}
    except Exception as e:
        return {"error": str(e)}


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt  #  POST 요청을 받을 수 있도록 CSRF 검사 비활성화 (테스트 시 사용)
def post_input(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # JSON 데이터 파싱
            # print("🔹 받은 데이터:", data)  #  콘솔에서 데이터 확인=> 삭제해도됨
            return JsonResponse({"message": "데이터 수신 완료", "status": "success", "received_data": data}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON 형식 오류"}, status=400)
    
    return JsonResponse({"error": "POST 요청만 허용됩니다."}, status=405)


#6번 섹션 (0129 새로 짬)
import os
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content

@csrf_exempt
def gen_cody(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            outfit_data = data.get('data', {})
            
            # 계절 판단 (월 기준)
            from datetime import datetime
            current_month = datetime.now().month
            if 3 <= current_month <= 5:
                season = "봄"
            elif 6 <= current_month <= 8:
                season = "여름"
            elif 9 <= current_month <= 11:
                season = "가을"
            else:
                season = "겨울"
            
            # 날씨 정보 초기화
            weather_info = ""
            try:
                # 날씨 정보 가져오기
                weather_data = get_weather_data(request)
                if isinstance(weather_data, JsonResponse):
                    weather_data = json.loads(weather_data.content)
                
                # 날씨 데이터가 있는 경우에만 처리
                if 'main' in weather_data and 'weather' in weather_data:
                    current_temp = weather_data.get('main', {}).get('temp', 0)
                    weather_condition = weather_data.get('weather', [{}])[0].get('description', '')
                    
                    # 날씨 정보 문자열 생성
                    weather_info = f"""
                    - 기온: {current_temp}°C
                    - 날씨 상태: {weather_condition}
                    """
            except Exception as e:
                logger.warning(f"날씨 정보를 가져오는데 실패했습니다: {str(e)}")
            
            # 사용자 정보 가져오기
            user = request.user
            user_info = {
                'gender': user.get_gender_display() if user.gender else "미지정",
                'age': f"{user.age}세" if user.age else "미지정",
                'height': f"{user.height}cm" if user.height else "미지정",
                'weight': user.get_weight_display() if user.weight else "미지정",
                'style': user.get_style_display() if user.style else "미지정"
            }

            # Google GenAI 클라이언트 초기화
            genai.configure(api_key=settings.INPUT_API_KEY)
            
            # 모델 설정
            generation_config = {
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
            }
            
            model = genai.GenerativeModel(
                model_name="gemini-1.5-pro-001",
                generation_config=generation_config,
            )

            prompt = f"""
            다음 정보를 바탕으로 무신사 스탠다드 제품으로 코디를 추천해주세요:

            1. 현재 환경 정보:
            - 계절: {season}
            {weather_info if weather_info else "- 날씨 정보를 가져올 수 없습니다"}

            2. 사용자 정보:
            - 성별: {user_info['gender']}
            - 나이: {user_info['age']}
            - 키: {user_info['height']}
            - 체중: {user_info['weight']}
            - 선호 스타일: {user_info['style']}

            3. 현재 선택한 의류 정보:
            {json.dumps(outfit_data, ensure_ascii=False)}

            위 정보를 고려하여:
            1. {season}에 적합하고, {'현재 날씨를 고려하여, ' if weather_info else ''}사용자의 체형과 스타일 선호도에 맞는 코디
            2. 선택한 의류와 어울리는 코디를 추천해주세요.

            다음 형식으로 출력해주세요:
            코디 1:
            - 상의: [제품명] - [구매링크]
            - 하의: [제품명] - [구매링크]
            - 신발: [제품명] - [구매링크]
            - 액세서리: [제품명] - [구매링크]

            코디 2:
            ...

            각 코디마다 왜 이 조합을 추천하는지 간단한 이유를 덧붙여주세요.
            무신사 스탠다드 제품으로만 추천해주세요.
            """

            chat_session = model.start_chat()
            response = chat_session.send_message(prompt)
            
            if response and response.text:
                return JsonResponse({
                    "cody_recommendation": response.text
                })
            else:
                return JsonResponse({"error": "추천 결과를 생성하지 못했습니다."}, status=500)

        except Exception as e:
            logger.error(f"Error in gen_cody: {str(e)}", exc_info=True)
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "POST 요청만 허용됩니다."}, status=405)

