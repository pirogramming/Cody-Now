from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm

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
                return render(request, 'user/login.html', {'form': form, 'invalid_creds': True})
    else:
        form = CustomAuthenticationForm()
    return render(request, 'user/login.html', {'form': form})

@login_required
def dashboard_view(request):
    return render(request, 'closet/dashboard.html') 
