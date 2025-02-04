from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model 
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomAuthenticationForm, SignUpForm, UserProfileUpdateForm
from django.contrib.auth.decorators import login_required

User = get_user_model()

# 회원가입
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # 사용자 생성
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('closet:dashboard')
    else:
        form = SignUpForm()
    return render(request, 'user/signup.html', {'form': form})

# 로그아웃
def logout_view(request):
    logout(request)
    return redirect('closet:dashboard')

# 로그인
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # 이메일 로그인
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

# 대시보드
@login_required
def dashboard_view(request):
    username = request.user.nickname  # CustomUser 모델의 nickname 필드 사용
    return render(request, "closet/dashboard.html", {"user": request.user})

# 사용자 프로필 보기
@login_required
def user_profile_view(request):
    user = request.user  # 로그인한 사용자
    if request.method == "POST":
        form = UserProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("closet:dashboard")
    else:
        form = UserProfileUpdateForm(instance=user)
    return render(request, "user_profile.html", {"form": form})

# 사용자 프로필 수정
@login_required
def edit_profile_view(request):
    if request.method == "POST":
        form = UserProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("closet:dashboard")
    else:
        form = UserProfileUpdateForm(instance=request.user)
    return render(request, "edit_profile.html", {"form": form})


