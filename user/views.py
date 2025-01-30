from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout,  get_user_model 
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView

from .forms import UserProfileForm, UserProfileUpdateForm

from .tokens import password_reset_token_generator 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.utils.encoding import force_bytes 
from django.urls import reverse 
from django.core.mail import send_mail 


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # 폼에서 사용자 생성: 이때 form은 이메일과 username 모두 받아야 함
            # 예시로 form.cleaned_data에서 이메일을 가져옴
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('closet:dashboard')
    else:
        form = SignUpForm()
    return render(request, 'user/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('closet:dashboard')

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # 여기서 'username'은 실제로 이메일 값입니다.
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('closet:dashboard')
            else:
                return render(request, 'account/login.html', {'form': form, 'invalid_creds': True})
    else:
        form = CustomAuthenticationForm()
    return render(request, 'account/login.html', {'form': form})

@login_required
def dashboard_view(request):
    username = request.user.nickname
    return render(request, "closet/dashboard.html", {"user": request.user})


@login_required
def user_profile_view(request):
    user = request.user  # ✅ 현재 로그인한 사용자

    if request.method == "POST":
        form = UserProfileUpdateForm(request.POST, instance=user)  # ✅ 기존 데이터 업데이트
        if form.is_valid():
            form.save()
            return redirect("closet:dashboard")  # ✅ 프로필 저장 후 대시보드 이동
        else:
            print("폼이 유효하지 않음:", form.errors)  # ✅ 디버깅을 위해 에러 출력

    else:
        form = UserProfileUpdateForm(instance=user)  # ✅ 기존 정보 불러오기

    return render(request, "user_profile.html", {"form": form})

@login_required
def edit_profile_view(request):
    if request.method == "POST":
        form = UserProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("closet:dashboard")  # ✅ 프로필 수정 후 대시보드로 이동
    else:
        form = UserProfileUpdateForm(instance=request.user)

    return render(request, "edit_profile.html", {"form": form})

User = get_user_model()

class CustomPasswordResetView(PasswordResetView):
    """
    비밀번호 재설정 이메일 전송 커스텀 뷰
    """
    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user = User.objects.filter(email=email).first()

        if user:
            token = password_reset_token_generator.make_token(user)  # ✅ 5분 제한된 토큰 생성
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            reset_url = self.request.build_absolute_uri(
                reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token})
            )

            # 이메일 전송
            send_mail(
                "비밀번호 재설정",
                f"아래 링크를 클릭하여 비밀번호를 재설정하세요:\n\n{reset_url}\n\n"
                "이 링크는 5분 후에 만료됩니다.",
                "noreply@yourdomain.com",
                [email],
                fail_silently=False,
            )

        return redirect("password_reset_done")  # ✅ 이메일 전송 후 완료 페이지로 이동
    
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    비밀번호 재설정 링크 클릭 시, 토큰이 만료되었는지 확인
    """
    def dispatch(self, request, *args, **kwargs):
        uidb64 = kwargs.get("uidb64")
        token = kwargs.get("token")

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and password_reset_token_generator.check_token(user, token):
            return super().dispatch(request, *args, **kwargs)
        else:
            return render(request, "password_reset_expired.html")  # ✅ 만료된 경우 에러 페이지로 이동