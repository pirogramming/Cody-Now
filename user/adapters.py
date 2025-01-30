from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_field
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
import random
import string

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    - 소셜 로그인 시 자동 계정 연결 방지
    - 제공자별로 username을 다르게 설정
    - 회원가입 후 프로필 페이지로 이동
    """

    def populate_user(self, request, sociallogin, data):
        """
        소셜 로그인 데이터를 가져와 사용자 객체를 생성하는 메서드
        """
        user = super().populate_user(request, sociallogin, data)
        
        provider = sociallogin.account.provider
        name = data.get("name", "")  
        
        if not user.username:
    
            unique_id = "".join(random.choices(string.digits, k=4))  # 랜덤 4자리 숫자 추가
            user.username = f"{name}_{provider}_{unique_id}"  # 예: leisure1566_google_1234

        user_field(user, "nickname", name) 
        return user

    def is_auto_signup_allowed(self, request, sociallogin):
        """
        자동 회원가입을 방지하여, 동일 이메일이 있어도 새 계정 생성하도록 설정
        """
        return False  # 자동 계정 연결 방지

    def get_login_redirect_url(self, request):

        return reverse("user_profile")  