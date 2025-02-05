from django.shortcuts import render, redirect, get_object_or_404
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
import traceback
import sys

from closet.models import Outfit, UserCategory, MyCloset

import google.generativeai as genai
from PIL import Image  # Pillow 라이브러리 추가
import pillow_heif  # HEIC 지원을 위해 추가
from io import BytesIO
from .custom_search import update_product_links, convert_markdown_to_html

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

#나만의 옷장 카테고리 관련
@csrf_exempt
def usercategory_view(request):
    user_categories = UserCategory.objects.filter(user=request.user)
    return JsonResponse({"categories": list(user_categories.values("id", "name","user"))})  # ✅ JSON으로 반환

def add_category(request):
    """사용자가 새로운 카테고리를 추가할 수 있도록 처리"""
    if request.method == "POST":
        data = json.loads(request.body)
        category_name = data.get("name")

        if not category_name:
            return JsonResponse({"success": False, "error": "카테고리 이름을 입력하세요."})

        if UserCategory.objects.filter(name=category_name, user=request.user).exists():
            return JsonResponse({"success": False, "error": "이미 존재하는 카테고리입니다."})

        category = UserCategory.objects.create(name=category_name, user=request.user)  # ✅ user 추가
        return JsonResponse({"success": True, "id": category.id})

    return JsonResponse({"success": False, "error": "잘못된 요청입니다."})

def delete_category(request):
    """사용자가 선택한 카테고리를 삭제하는 API"""
    if request.method == "POST":
        data = json.loads(request.body)
        category_id = data.get("id")

        if not category_id:
            return JsonResponse({"success": False, "error": "카테고리 ID가 필요합니다."})

        try:
            category = UserCategory.objects.get(id=category_id)
            category.delete()
            return JsonResponse({"success": True})
        except UserCategory.DoesNotExist:
            return JsonResponse({"success": False, "error": "해당 카테고리가 존재하지 않습니다."})

    return JsonResponse({"success": False, "error": "잘못된 요청입니다."})

@login_required
def save_outfit_to_closet(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            outfit_id = data.get("outfit_id")
            category_ids = data.get("category_ids")
            user = request.user

            if not outfit_id or not category_ids:
                return JsonResponse({"success": False, "error": "필수 데이터가 부족합니다."})

            # ✅ Outfit 객체 가져오기
            try:
                outfit = Outfit.objects.get(id=outfit_id)
            except Outfit.DoesNotExist:
                return JsonResponse({"success": False, "error": "해당 Outfit이 존재하지 않습니다."})

            # ✅ 선택한 모든 카테고리에 대해 저장
            for category_id in category_ids:
                try:
                    user_category = UserCategory.objects.get(id=category_id, user=user)
                    MyCloset.objects.create(user=user, outfit=outfit, user_category=user_category)
                except UserCategory.DoesNotExist:
                    return JsonResponse({"success": False, "error": "해당 카테고리가 존재하지 않습니다."})

            return JsonResponse({"success": True, "message": "나만의 옷장에 성공적으로 저장되었습니다!"})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "잘못된 JSON 형식입니다."})

    return JsonResponse({"success": False, "error": "잘못된 요청 방식입니다."})

#날씨 관련
def weather_view(request):
    return render(request, 'weather.html')

def get_weather_data(request):
    api_key = settings.OPENWEATHER_API_KEY
    # 서울의 기본 위도/경도
    default_lat = "37.5665"
    default_lon = "126.9780"
    
    lat = request.GET.get('lat', default_lat)
    lon = request.GET.get('lon', default_lon)
    
    # 도시 이름으로 검색하는 경우
    city = request.GET.get('city')
    if city:
        # 도시 이름으로 좌표 검색
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
        try:
            geo_response = requests.get(geo_url)
            geo_data = geo_response.json()
            if geo_data:
                lat = geo_data[0]['lat']
                lon = geo_data[0]['lon']
        except Exception as e:
            return JsonResponse({'error': f'도시를 찾을 수 없습니다: {str(e)}'}, status=400)

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

def process_image(image_file):
    """
    이미지 파일을 처리하고 최적화하는 함수
    - 지원 포맷: PNG, JPEG, WEBP, HEIC
    - 20MB 이상 파일 자동 최적화
    - HEIC를 JPEG로 자동 변환
    """
    MAX_SIZE = 20 * 1024 * 1024  # 20MB in bytes
    SUPPORTED_FORMATS = {'PNG', 'JPEG', 'JPG', 'WEBP', 'HEIC'}
    
    try:
        # 파일 확장자 확인
        ext = image_file.name.split('.')[-1].upper()
        if ext not in SUPPORTED_FORMATS:
            raise ValidationError(f"지원하지 않는 이미지 형식입니다. 지원 형식: {', '.join(SUPPORTED_FORMATS)}")

        # HEIC 처리
        if ext == 'HEIC':
            heif_file = pillow_heif.read_heif(image_file)
            image = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                "raw",
            )
        else:
            image = Image.open(image_file)

        # 이미지 모드 확인 및 변환
        if image.mode not in ('RGB', 'RGBA'):
            image = image.convert('RGB')

        # 파일 크기 확인 및 최적화
        img_byte_arr = BytesIO()
        
        if ext in ['PNG', 'WEBP']:
            image.save(img_byte_arr, format='PNG', optimize=True)
        else:
            image.save(img_byte_arr, format='JPEG', quality=85, optimize=True)
        
        img_byte_arr.seek(0)
        file_size = img_byte_arr.getbuffer().nbytes

        # 20MB 초과시 추가 최적화
        if file_size > MAX_SIZE:
            quality = 85
            while file_size > MAX_SIZE and quality > 20:
                img_byte_arr = BytesIO()
                image.save(img_byte_arr, format='JPEG', quality=quality, optimize=True)
                img_byte_arr.seek(0)
                file_size = img_byte_arr.getbuffer().nbytes
                quality -= 5

        return img_byte_arr

    except Exception as e:
        raise ValidationError(f"이미지 처리 중 오류가 발생했습니다: {str(e)}")

@csrf_exempt
#@login_required
def upload_outfit(request):
    if request.method == 'POST':
        form = OutfitForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # 이미지 처리
                processed_image = process_image(form.cleaned_data['image'])
                
                # Outfit 객체 생성 및 저장
                outfit = Outfit(user=request.user)
                
                # 처리된 이미지를 임시 파일로 저장
                temp_name = f"processed_{get_valid_filename(form.cleaned_data['image'].name)}"
                if not temp_name.lower().endswith(('.jpg', '.jpeg')):
                    temp_name = f"{os.path.splitext(temp_name)[0]}.jpg"
                
                outfit.image.save(temp_name, processed_image, save=False)
                outfit.save()
                
                # Gemini API 호출
                with open(outfit.image.path, "rb") as img_file:
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
                     "outfit_id": outfit.id,
                    "data": analysis_result
                })
            
            except ValidationError as e:
                logger.error(f"Validation Error: {str(e)}", exc_info=True)
                return JsonResponse({
                    "error": str(e),
                    "error_details": traceback.format_exc()
                }, status=400)
            except Exception as e:
                logger.error(f"Error in upload_outfit: {str(e)}", exc_info=True)
                return JsonResponse({
                    "error": str(e),
                    "error_details": traceback.format_exc()
                }, status=500)
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
            
            # 업로드된 이미지 URL 가져오기
            outfit_id = outfit_data.get('outfit_id')
            uploaded_image_url = None
            if outfit_id:
                outfit = Outfit.objects.get(id=outfit_id)
                if outfit.image:
                    uploaded_image_url = outfit.image.url
                elif outfit.image_url:
                    uploaded_image_url = outfit.image_url
            
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
                'weight': f"{user.weight}kg" if user.weight else "미지정",
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
            markdown 형식을 준수해주세요. 사용자에게 친근한 느낌으로 추천해주세요. 브랜드 이름 `무신사 스탠다드)` 제품 명 앞에 표기해주세요. 색상은 추천할 필요 없고 제품 명만 추천해주세요
            예시)
            ``` 
            - 하의: [무신사 스탠다드 베이식 릴렉스 스웨트팬츠 블랙](https://www.musinsa.com/app/goods/2444794/0) - 후드티와 같은 블랙 컬러 스웨트팬츠로 통일감을 주면서 편안한 무드를 연출! 릴렉스 핏으로 활동성도 높여줍니다.
            ```
            반드시 무신사 스탠다드 제품으로만 추천해주세요. 사용자가 업로드해서 추천할 필요가 없을 때에는 `(현재 업로드하신 옷)` 이라고 출력해주세요.   
            TYPE 1:
            - 상의: [무신사 스탠다드 - 제품명(구매링크)
            - 하의: [무신사 스탠다드 - 제품명(구매링크)
            - 신발: [무신사 스탠다드 - 제품명(구매링크)


            TYPE 2:
            ...

            각 코디마다 왜 이 조합을 추천하는지 간단한 이유를 덧붙여주세요.
            무신사 스탠다드 제품으로만 추천해주세요.
            """

            chat_session = model.start_chat()
            response = chat_session.send_message(prompt)
            
            if response and response.text:
                # 원본 마크다운 텍스트 저장
                original_markdown = response.text
                
                # custom_search 함수들로 처리
                updated_markdown = update_product_links(
                    original_markdown, 
                    user=request.user if request.user.is_authenticated else None,
                    uploaded_image_url=uploaded_image_url
                )
                html_content = convert_markdown_to_html(updated_markdown)
                
                return JsonResponse({
                    "original_text": original_markdown,  # 원본 텍스트 추가
                    "cody_recommendation": html_content
                })
            else:
                return JsonResponse({"error": "추천 결과를 생성하지 못했습니다."}, status=500)

        except Exception as e:
            logger.error(f"Error in gen_cody: {str(e)}", exc_info=True)
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "POST 요청만 허용됩니다."}, status=405)

# @login_required
# def evaluate_closet(request):
#     try:
#         # 현재 로그인한 사용자의 옷장 정보 가져오기
#         outfits = Outfit.objects.filter(user=request.user)

#         if not outfits.exists():
#             return render(request, "closet/evaluate_closet.html", {
#                 "closet_evaluation": "옷장에 저장된 옷이 없습니다. 먼저 옷을 추가해 주세요!"
#             })

#         # 옷 데이터 추출 (스타일, 카테고리, 색상 등)
#         outfit_data = []
#         for outfit in outfits:
#             outfit_data.append({
#                 "design_style": outfit.design_style or "알 수 없음",
#                 "category": outfit.category or "알 수 없음",
#                 "color": outfit.color or "알 수 없음",
#                 "fit": outfit.fit or "알 수 없음",
#                 "material": outfit.material or "알 수 없음",
#                 "season": outfit.season or "알 수 없음"
#             })

#         # Gemini API 프롬프트 생성
#         prompt = f"""
#         사용자의 옷장 데이터를 분석하여 옷장 스타일을 평가하세요.

#         - 주로 어떤 스타일의 옷이 많은지 분석하세요.
#         - 특정 스타일이 많다면 그 스타일을 강조해서 평가해 주세요. (예: "캐주얼한 옷이 많네요! 캐주얼 스타일을 좋아하시나요?")
#         - 다양한 스타일이 섞여 있다면, 적절한 코멘트를 작성하세요.
#         - 아래 데이터 기반으로 평가해주세요.

#         사용자의 옷장 데이터:
#         {json.dumps(outfit_data, ensure_ascii=False)}

#         평가를 한 문장으로 요약해서 출력하세요.
#         """

#         # Google GenAI API 호출
#         genai.configure(api_key=settings.GEMINI_API_KEY)  # ✅ 환경 변수에서 API 키 가져오기
#         model = genai.GenerativeModel("gemini-1.5-pro-001")
#         response = model.generate_content(prompt)

#         # 응답 처리
#         evaluation_result = response.text if response and response.text else "Gemini API에서 평가를 생성하지 못했습니다."

#         # 평가 결과를 템플릿에 전달하여 렌더링
#         return render(request, "closet/evaluate_closet.html", {
#             "closet_evaluation": evaluation_result
#         })

#     except Exception as e:
#         return render(request, "closet/evaluate_closet.html", {
#             "closet_evaluation": f"오류 발생: {str(e)}"
#         })

import json
import google.generativeai as genai
from django.core.cache import cache
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render
from closet.models import Outfit


@login_required
def evaluate_closet(request):
    try:
        user = request.user
        cache_key = f"closet_evaluation_{user.id}"  # 캐시 키 (사용자 ID 기반)
        last_update_key = f"closet_last_update_{user.id}"  # 마지막 변경 시간 키

        # DB에서 마지막 Outfit 업데이트 시간 확인
        last_outfit = Outfit.objects.filter(user=user).order_by('-created_at').first()
        last_update_time = last_outfit.created_at if last_outfit else None

        # 캐시된 데이터와 마지막 업데이트 시간 비교
        cached_data = cache.get(cache_key)
        cached_update_time = cache.get(last_update_key)

        if cached_data and cached_update_time == last_update_time:
            print("✅ 캐시된 평가 결과 반환")
            return render(request, "closet/evaluate_closet.html", {
                "closet_evaluation": cached_data
            })

        # 새로운 평가가 필요한 경우
        outfits = Outfit.objects.filter(user=user)

        if not outfits.exists():
            return render(request, "closet/evaluate_closet.html", {
                "closet_evaluation": "옷장에 저장된 옷이 없습니다. 먼저 옷을 추가해 주세요!"
            })

        # 옷 데이터 추출 (스타일, 카테고리, 색상 등)
        outfit_data = []
        for outfit in outfits:
            outfit_data.append({
                "design_style": outfit.design_style or "알 수 없음",
                "category": outfit.category or "알 수 없음",
                "color": outfit.color or "알 수 없음",
                "fit": outfit.fit or "알 수 없음",
                "material": outfit.material or "알 수 없음",
                "season": outfit.season or "알 수 없음"
            })

        # Gemini API 프롬프트 생성
        prompt = f"""
        사용자의 옷장 데이터를 분석하여 옷장 스타일을 평가하세요.

        - 주로 어떤 스타일의 옷이 많은지 분석하세요.
        - 특정 스타일이 많다면 그 스타일을 강조해서 평가해 주세요. (예: "캐주얼한 옷이 많네요! 캐주얼 스타일을 좋아하시나요?")
        - 다양한 스타일이 섞여 있다면, 적절한 코멘트를 작성하세요.
        - 아래 데이터 기반으로 평가해주세요.

        사용자의 옷장 데이터:
        {json.dumps(outfit_data, ensure_ascii=False)}

        평가를 한 문장으로 요약해서 출력하세요.
        """

        # Gemini API 호출
        genai.configure(api_key=settings.INPUT_API_KEY)  
        model = genai.GenerativeModel("gemini-1.5-pro-001")
        response = model.generate_content(prompt)

        evaluation_result = response.text if response and response.text else "Gemini API에서 평가를 생성하지 못했습니다."

        # 캐시에 저장 (변경 시간 포함)
        cache.set(cache_key, evaluation_result, timeout=None)  
        cache.set(last_update_key, last_update_time, timeout=None)

        return render(request, "closet/evaluate_closet.html", {
            "closet_evaluation": evaluation_result
        })

    except Exception as e:
        return render(request, "closet/evaluate_closet.html", {
            "closet_evaluation": f"오류 발생: {str(e)}"
        })
    


    ###closet_main 페이지 : main, 삭제, 북마크

@login_required
def closet_main(request):
    user = request.user
    show_bookmarked = request.GET.get('bookmarked', 'false').lower() == 'true'  # 북마크 필터 확인

    if show_bookmarked:
        outfits = Outfit.objects.filter(user=user, bookmarked=True).order_by('-created_at')
    else:
        outfits = Outfit.objects.filter(user=user).order_by('-created_at')

    return render(request, 'closet/closet_main.html', {
        'outfits': outfits, 'show_bookmarked': show_bookmarked
        })

@login_required
def toggle_bookmark(request, outfit_id):
 
    if request.method == "POST":
        # 로그인한 사용자의 outfit만 처리하도록 필터링합니다.
        outfit = get_object_or_404(Outfit, pk=outfit_id, user=request.user)
        outfit.bookmarked = not outfit.bookmarked
        outfit.save()
        return JsonResponse({
            "message": "북마크 상태가 변경되었습니다.",
            "bookmarked": outfit.bookmarked
        })
    else:
        return JsonResponse({"error": "유효하지 않은 요청입니다."}, status=400)


@login_required
def delete_outfit(request, outfit_id):

    if request.method == "POST":
        outfit = get_object_or_404(Outfit, pk=outfit_id, user=request.user)
        outfit.delete()
        return JsonResponse({"message": "옷이 성공적으로 삭제되었습니다."})
    else:
        return JsonResponse({"error": "유효하지 않은 요청입니다."}, status=400)
    
def custom_500_error(request):
    """500 에러 핸들러"""
    error_info = ""
    if settings.DEBUG:
        # 현재 발생한 예외 정보 가져오기
        error_type, error_value, tb = sys.exc_info()
        
        # 트레이스백을 문자열로 변환
        error_traceback = ''.join(traceback.format_tb(tb))
        
        error_info = f"""
        Error Type: {error_type.__name__ if error_type else 'Unknown'}
        Error Message: {str(error_value)}
        
        Traceback:
        {error_traceback}
        
        Request Method: {request.method}
        Request Path: {request.path}
        User: {request.user}
        """
        
        # 로그에도 기록
        logger.error(error_info)
    
    return render(request, '500.html', {
        'error_info': error_info,
        'debug': settings.DEBUG
    }, status=500)

# urls.py에 등록할 핸들러
handler500 = 'closet.views.custom_500_error'


def get_outfit_data(request, outfit_id):
    try:
        outfit = Outfit.objects.get(id=outfit_id)
        return JsonResponse({
            "image_url": outfit.image.url if outfit.image else "",
            "analysis_result": outfit.raw_response,  # AI 분석 결과
            "cody_recommendation": outfit.comment  # 코디 추천 결과 (필요 시)
        })
    except Outfit.DoesNotExist:
        return JsonResponse({"error": "해당 옷 정보를 찾을 수 없습니다."}, status=404)
    



#테스트해볼 때 이미지 업로드
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

#def test_image_upload(request):
    # if request.method == "POST" and request.FILES.get("image"):
    #     image = request.FILES["image"]
    #     file_path = f"temp_uploads/{image.name}"
    #     file_name = default_storage.save(file_path, ContentFile(image.read()))
    #     request.session["temp_image_url"] = default_storage.url(file_name)  # 세션에 이미지 URL 저장
    #     request.session.modified = True
    #     return redirect("test_input_page")  # 업로드 후 test_input.html로 리디렉션

    # temp_image_url = request.session.get("temp_image_url", None)  # 기존 업로드 이미지 가져오기
    # return render(request, "closet/test_input.html", {"temp_image_url": temp_image_url})
    #두 번째로 한 방법 
    # if request.method == "POST" and request.FILES.get("image"):
    #     image = request.FILES["image"]
    #     # TODO: 이미지 처리 로직 추가 (예: AI 모델 호출)
        
    #     # 예제 응답
    #     return JsonResponse({"message": "이미지 분석 완료", "analysis_result": {"color": "blue", "pattern": "striped"}})
    
    # return JsonResponse({"error": "이미지를 업로드해주세요."}, status=400)

# def test_image_upload(request):
#     if request.method == "POST" and request.FILES.get("image"):
#         image = request.FILES["image"]
#         print("업로드된 이미지:", image.name)  # 서버 로그 확인용
        
#         # 이미지 저장 (테스트용)
#         file_path = f"temp_uploads/{image.name}"
#         file_name = default_storage.save(file_path, ContentFile(image.read()))
#         temp_image_url = default_storage.url(file_name)

#         # 예제 AI 분석 결과
#         response_data = {
#             "message": "이미지 분석 완료",
#             "temp_image_url": temp_image_url,
#             "analysis_result": {"color": "blue", "pattern": "striped"}
#         }
#         print(" 반환 데이터:", response_data)  # 서버 로그 확인용
        
#         return JsonResponse(response_data)

#     print("이미지 업로드 실패: 파일 없음")
#     return JsonResponse({"error": "이미지를 업로드해주세요."}, status=400)
import json
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
# get_weather_data, call_gemini_api, genai, settings, logger 는 미리 임포트되어 있다고 가정합니다.

@csrf_exempt
def test_image_upload(request):
    """
    이 함수는 로그인하지 않아도 이용할 수 있는 체험하기 함수입니다람쥐
    업로드된 옷 이미지를 받아서
    1. Gemini API를 통해 이미지 분석을 수행하고, 
    2. 분석 결과를 바탕으로 무신사 스탠다드 제품 코디를 추천합니다.
    """
    if request.method != 'POST':
        return JsonResponse({"error": "POST 요청만 허용됩니다."}, status=405)

    try:
        # 1. 요청 데이터 파싱 및 이미지 추출
        if request.content_type.startswith("application/json"):
            # JSON 데이터인 경우
            try:
                data = json.loads(request.body.decode('utf-8'))
            except UnicodeDecodeError as e:
                return JsonResponse({"error": f"JSON 디코딩 오류: {str(e)}"}, status=400)
            base64_image = data.get("image")
        elif request.content_type.startswith("multipart/form-data"):
            # 파일 업로드인 경우: request.FILES 에서 파일 읽고 base64로 인코딩
            if "image" in request.FILES:
                image_file = request.FILES["image"]
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            else:
                return JsonResponse({"error": "이미지 파일이 제공되지 않았습니다."}, status=400)
        else:
            return JsonResponse({"error": "지원하지 않는 Content-Type 입니다."}, status=400)

        if not base64_image:
            return JsonResponse({"error": "이미지 데이터가 제공되지 않았습니다."}, status=400)

        # 2. 업로드된 이미지 분석 (call_gemini_api 함수 사용)
        analysis_result = call_gemini_api(base64_image)
        if analysis_result.get("error"):
            return JsonResponse(analysis_result, status=500)
        outfit_data = analysis_result

        # 3. 현재 환경 정보 설정 (계절 판단)
        current_month = datetime.now().month
        if 3 <= current_month <= 5:
            season = "봄"
        elif 6 <= current_month <= 8:
            season = "여름"
        elif 9 <= current_month <= 11:
            season = "가을"
        else:
            season = "겨울"

        # 4. 날씨 정보 가져오기
        weather_info = ""
        try:
            weather_data = get_weather_data(request)
            if isinstance(weather_data, JsonResponse):
                weather_data = json.loads(weather_data.content)
            if 'main' in weather_data and 'weather' in weather_data:
                current_temp = weather_data.get('main', {}).get('temp', 0)
                weather_condition = weather_data.get('weather', [{}])[0].get('description', '')
                weather_info = f"- 기온: {current_temp}°C\n- 날씨 상태: {weather_condition}"
        except Exception as e:
            logger.warning(f"날씨 정보를 가져오는데 실패했습니다: {str(e)}")

        # 5. 로그인 없이 체험할 수 있도록 기본 사용자 정보 사용
        user_info = {
            'gender': "미지정",
            'age': "미지정",
            'height': "미지정",
            'weight': "미지정",
            'style': "미지정"
        }

        # 6. Google Gemini API 클라이언트 초기화 및 모델 설정
        genai.configure(api_key=settings.INPUT_API_KEY)
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

        # 7. 코디 추천 프롬프트 생성
        prompt = f"""
        다음 정보를 바탕으로 무신사 스탠다드 제품으로 코디를 추천해주세요:

        1. 현재 환경 정보:
        - 계절: {season}
        {"- " + weather_info if weather_info else "- 날씨 정보를 가져올 수 없습니다."}

        2. 사용자 정보:
        - 성별: {user_info['gender']}
        - 나이: {user_info['age']}
        - 키: {user_info['height']}
        - 체중: {user_info['weight']}
        - 선호 스타일: {user_info['style']}

        3. 현재 선택한 의류 정보 (이미지 분석 결과):
        {json.dumps(outfit_data, ensure_ascii=False, indent=2)}

        위 정보를 고려하여:
        1. {season}에 적합하고, {"현재 날씨를 고려하여, " if weather_info else ""}사용자 체형 및 스타일에 맞는 코디
        2. 선택한 의류와 어울리는 코디를 추천해주세요.
        
        아래 형식을 준수하여 출력해주세요:
        - markdown 형식을 사용
        - 브랜드 이름 `무신사 스탠다드` 제품명 앞에 표기하고 구매 링크 포함 (예: [무신사 스탠다드 와이드 히든 밴딩 스웨트팬츠 오트밀](https://www.musinsa.com/app/goods/2767065))
        - 반드시 무신사 스탠다드 제품으로만 추천해주세요.
        - (만약 업로드하신 옷과 관련된 추천이 필요없다면 `(현재 업로드하신 옷)` 이라고 출력해주세요.)

        TYPE 1:
        - 상의: [무신사 스탠다드 - 제품명(구매링크)]
        - 하의: [무신사 스탠다드 - 제품명(구매링크)]
        - 신발: [무신사 스탠다드 - 제품명(구매링크)]

        TYPE 2:
        ...

        각 코디마다 추천 이유를 간단히 덧붙여주세요.
        """

        # 8. Gemini API를 통해 코디 추천 생성
        chat_session = model.start_chat()
        response = chat_session.send_message(prompt)
        if response and response.text:
            updated_markdown = update_product_links(
                response.text, 
                user=request.user if request.user.is_authenticated else None,
                uploaded_image_url=uploaded_image_url
            )
            html_content = convert_markdown_to_html(updated_markdown)
            
            return JsonResponse({
                "analysis_result": outfit_data,
                "cody_recommendation": html_content
            })
        else:
            return JsonResponse({"error": "추천 결과를 생성하지 못했습니다."}, status=500)

    except Exception as e:
        logger.error(f"Error in test_image_upload: {str(e)}", exc_info=True)
        return JsonResponse({"error": str(e)}, status=500)

#test_input.html로 가도록
def test_input_page(request):
    """로그인하지 않은 사용자가 프로필 저장 후 이동할 테스트 페이지"""
    temp_image_url = request.session.get("temp_image_url", None)  # 세션에 저장된 이미지 가져오기
    return render(request, "closet/test_input.html", {"temp_image_url": temp_image_url})  