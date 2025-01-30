from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model
from django.urls import reverse
import random
import string

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    - 기존 소셜 계정이 있으면 새 계정 생성 없이 로그인 처리
    - 제공자별로 username을 다르게 설정하여 중복 방지
    - 최초 회원가입 시 프로필 페이지로 이동
    """

    def pre_social_login(self, request, sociallogin):
        """
        ✅ 기존 계정이 있을 경우 새로운 `SocialAccount`를 만들지 않고 연결
        """
        email = sociallogin.account.extra_data.get("email")  # ✅ 소셜 로그인에서 제공하는 이메일
        provider = sociallogin.account.provider  # ✅ Google, Naver 등 제공자 확인

        # ✅ 같은 이메일을 가진 기존 계정이 있는지 확인
        existing_user = User.objects.filter(email=email).first()
        if existing_user:
            # ✅ 기존 계정이 존재하면 현재 소셜 계정과 연결
            sociallogin.connect(request, existing_user)
            sociallogin.state["existing_user"] = True  # ✅ 로그인 처리 상태 추가
            return

    def populate_user(self, request, sociallogin, data):
        """
        ✅ 새로운 계정을 생성할 때, 중복된 username 방지
        """
        user = super().populate_user(request, sociallogin, data)
        provider = sociallogin.account.provider  # ✅ 네이버, 구글 등 제공자 확인
        name = data.get("name", "")  # ✅ 네이버/구글 API에서 가져온 이름

        if not user.username:
            base_username = f"{name}_{provider}"
            unique_username = base_username

            while User.objects.filter(username=unique_username).exists():
                unique_id = "".join(random.choices(string.digits, k=4))  # 랜덤 4자리 숫자 추가
                unique_username = f"{base_username}_{unique_id}"  # 예: leisure1566_google_1234

            user.username = unique_username  # ✅ 최종적으로 중복되지 않는 username 설정

        return user

    def get_login_redirect_url(self, request):
        """
        ✅ 최초 회원가입 시 프로필 페이지로 이동
        ✅ 기존 로그인 시 대시보드로 이동
        """
        user = request.user

        # ✅ 기존 로그인인지 확인 (pre_social_login에서 상태 체크)
        is_first_login = request.session.pop("is_first_login", False)

        if is_first_login:
            return reverse("user_profile")  # ✅ 프로필 페이지로 이동
        else:
            return reverse("closet:dashboard")  # ✅ 기존 로그인은 대시보드로 이동