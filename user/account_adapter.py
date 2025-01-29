from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model

class CustomAccountAdapter(DefaultAccountAdapter):
    """
    이메일이 이미 존재하면, 해당 계정과 소셜 계정을 자동으로 연결하는 어댑터
    """
    def is_open_for_signup(self, request):
        return True  # 회원가입 허용

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    소셜 로그인 시 이메일이 이미 존재하면 기존 계정과 연결
    """
    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        if user.email:
            try:
                existing_user = get_user_model().objects.get(email=user.email)
                sociallogin.connect(request, existing_user)  # 기존 계정과 소셜 계정 연결
            except get_user_model().DoesNotExist:
                pass  # 새로운 계정으로 가입 진행