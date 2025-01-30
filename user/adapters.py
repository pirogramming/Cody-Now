from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
import random
import string

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    - 소셜 로그인 시 자동 계정 연결 방지
    - 제공자별로 username을 다르게 설정하여 중복 방지
    - 이메일이 동일하더라도 새로운 계정을 생성하도록 설정
    """

    def populate_user(self, request, sociallogin, data):
        """
        소셜 로그인 데이터를 가져와 사용자 객체를 생성하는 메서드
        """
        user = super().populate_user(request, sociallogin, data)

        provider = sociallogin.account.provider  # ✅ 네이버, 구글 등 제공자 확인
        email = data.get("email", "")  # ✅ 소셜 로그인에서 제공하는 이메일
        name = data.get("name", "")  # ✅ 네이버/구글 API에서 가져온 이름

        # ✅ 새로운 계정을 생성하도록 처리 (기존 계정과 연결하지 않음)
        if User.objects.filter(email=email).exists():
            base_username = f"{name}_{provider}"
            unique_username = base_username

            # ✅ 중복된 username이 없을 때까지 랜덤한 숫자 추가
            while User.objects.filter(username=unique_username).exists():
                unique_id = "".join(random.choices(string.digits, k=4))  # 랜덤 4자리 숫자 추가
                unique_username = f"{base_username}_{unique_id}"  # 예: leisure1566_google_1234

            user.username = unique_username  # ✅ 최종적으로 중복되지 않는 username 설정
            user.email = email  # ✅ 올바른 이메일 설정
            user.save()  # ✅ 새로운 계정 생성

        return user

    def get_login_redirect_url(self, request):
        """
        ✅ 회원가입 후 프로필 페이지로 이동
        ✅ 기존 로그인 시 대시보드로 이동
        """
        user = request.user

        # ✅ 필수 정보가 비어있다면 회원가입 후 프로필 페이지로 이동
        if user and user.is_authenticated:
            if not user.first_name or not user.nickname or not user.age:
                return reverse("user_profile")  # ✅ 프로필 페이지로 이동
            else:
                return reverse("closet:dashboard")  # ✅ 기존 로그인은 대시보드로 이동

        return reverse("closet:dashboard")  # 기본적으로 대시보드로 이동