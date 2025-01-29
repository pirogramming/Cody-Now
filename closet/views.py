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





#5번 섹션(input)
from django.http import JsonResponse
from .forms import OutfitForm
from closet.models import Outfit
from django.conf import settings

import google.generativeai as genai
import os
import base64
import json
import requests



# 이미지 업로드 및 분석 View
def upload_outfit(request):
    api_key = "INPUT_API_KEY"
    genai.configure(api_key=settings.INPUT_API_KEY)
    if request.method == 'POST':
        form = OutfitForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            
            # outfits 디렉토리 경로 생성
            outfits_dir = os.path.join(settings.MEDIA_ROOT, 'outfits')
            
            # outfits 디렉토리가 없으면 생성
            if not os.path.exists(outfits_dir):
                os.makedirs(outfits_dir)
            
            # 이미지를 outfits 디렉토리에 저장
            image_path = os.path.join(outfits_dir, image.name)
            
            try:
                # 이미지 저장
                with open(image_path, "wb") as f:
                    for chunk in image.chunks():
                        f.write(chunk)
                        
                # 이미지 URL 생성 (outfits 디렉토리 포함)
                image_url = f"{settings.MEDIA_URL}outfits/{image.name}"

                # 이미지 Base64 인코딩
                with open(image_path, "rb") as img_file:
                    base64_image = base64.b64encode(img_file.read()).decode("utf-8")
                
                # Gemini 1.5 Pro API 요청
                response = call_gemini_api(base64_image)

                # 응답이 문자열(str)이라면 JSON 변환
                if isinstance(response, str) and response.strip():  # 빈 문자열 방지
                    try:
                        response = json.loads(response)
                    except json.JSONDecodeError as e:
                        return JsonResponse({"error": f"JSON 파싱 오류: {str(e)}", "raw_response": response}, status=500)
                
                #  API 응답 JSON에서 필요한 값 추출
                outfit = Outfit.objects.create(
                    design_style=response.get("design_style", ""),
                    category=response.get("category", ""),
                    overall_design=response.get("overall_design", ""),
                    logo_location=response.get("logo_or_lettering", {}).get("logo_location", ""),
                    logo_size=response.get("logo_or_lettering", {}).get("logo_size", ""),
                    logo_content=response.get("logo_or_lettering", {}).get("logo_content", ""),
                    color_and_pattern=response.get("color_and_pattern", ""),
                    color=response.get("color", ""),
                    fit=response.get("fit", ""),
                    cloth_length=response.get("cloth_length", ""),
                    neckline=response.get("neckline", ""),
                    detail=response.get("detail", ""),
                    material=response.get("material", ""),
                    season=response.get("season", ""),
                    tag=response.get("tag", []),
                    comment=response.get("comment", ""),
                    brand=response.get("brand", ""),
                    price=response.get("price", ""),
                    image_url=image_url  # 저장된 이미지 URL
                )


                #✅✅✅✅✅✅✅은경이 주목✅✅✅✅✅✅✅✅✅
                #  POST 요청을 보낼 URL (은경아 이거 수정해줘 너가 만든 post된거 받는 함수명으로 하면됨 urls도 수정해야하고)
                post_input_data_url = "http://127.0.0.1:8000/post_input/"  

                #  전송할 JSON 데이터
                post_input_data = {
                    "outfit_id": outfit.id,
                    "image_url": image_url,
                    "data": response
                }

                #  POST 요청 보내기 (타임아웃 설정 & 예외 처리)
                try:
                    post_input_data_response = requests.post(
                        post_input_data_url, json=post_input_data, timeout=5
                    )
                    post_input_data_response.raise_for_status()  # HTTP 오류 발생 시 예외 처리
                    post_input_data_result = post_input_data_response.json()  #  응답 JSON 변환
                except requests.exceptions.RequestException as e:
                    post_input_data_result = {"error": f"POST 요청 실패: {str(e)}"}




                return JsonResponse({
                    "message": "Outfit saved successfully",
                    "id": outfit.id,  # ✅ 저장된 데이터의 ID 반환
                    "image_url": image_url,  # ✅ 이미지 URL 반환
                    "data": response , # ✅ 분석된 데이터도 같이 반환
                    "post_input_data_result": post_input_data_result # ✅✅✅✅ 은경이에게 보낼 응답 포함
                }, safe=False)
            
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
    else:
        form = OutfitForm()
    
    return render(request, 'closet/input.html', {'form': form})



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


#✅✅✅✅✅✅은경아 여기 post_input함수명 바꾸려면 위에도 바꿔야해=> 기능은 너가 필요한대로 바꿔서 써✅✅✅✅✅✅✅✅

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt  #  POST 요청을 받을 수 있도록 CSRF 검사 비활성화 (테스트 시 사용)
def post_input(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # JSON 데이터 파싱
            print("🔹 받은 데이터:", data)  #  콘솔에서 데이터 확인=> 삭제해도됨
            return JsonResponse({"message": "데이터 수신 완료", "status": "success", "received_data": data}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON 형식 오류"}, status=400)
    
    return JsonResponse({"error": "POST 요청만 허용됩니다."}, status=405)


