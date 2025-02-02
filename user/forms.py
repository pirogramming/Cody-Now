from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import CustomUser

class CustomAuthenticationForm(AuthenticationForm):
    """
    로그인 폼 - 이메일을 아이디처럼 사용
    """
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': '이메일을 입력하세요'}),
        label="이메일"
    )

class SignUpForm(UserCreationForm):
    """
    회원가입 폼 - 이메일과 비밀번호만 입력받도록 변경
    """
    email = forms.EmailField(
        max_length=255,
        help_text="유효한 이메일 주소를 입력하세요."
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        help_text="최소 8자 이상의 비밀번호를 입력하십시오"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        help_text="같은 비밀번호를 한번 더 입력하십시오"
    )

    class Meta:
        model = get_user_model()
        fields = ("email", "password1", "password2")  # ✅ username 제거

class UserProfileForm(forms.ModelForm):
    """
    프로필 입력 폼 (회원가입 후 추가 정보 입력)
    """
    class Meta:
        model = CustomUser
        fields = ["nickname", "gender", "age", "height", "weight"]
        widgets = {
            "gender": forms.RadioSelect(choices=CustomUser.GENDER_CHOICES),
            "weight": forms.NumberInput(attrs={"class": "form-control", "placeholder": "몸무게 입력 (kg)"}),
        }


from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import CustomUser

class UserProfileUpdateForm(forms.ModelForm):
    GENDER_CHOICES = [
        ("", "성별 선택"), 
        ("M", "남성"),
        ("F", "여성"),
    ]

    STYLE_CHOICES = [
        ("", "스타일 선택"),  
        ("noidea", "잘 모르겠어요"),
        ("casual", "캐주얼"),
        ("formal", "포멀"),
        ("sporty", "스포티"),
        ("street", "스트릿"),
    ]

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(),
        required=True
    )

    style = forms.ChoiceField(
        choices=STYLE_CHOICES[1:],  # 🔥 기본 선택값 (빈 값) 제거
        widget=forms.Select(),
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ["nickname", "gender", "age", "height", "weight", "style"]
        widgets = {
            "nickname": forms.TextInput(attrs={"class": "form-control", "placeholder": "닉네임 입력"}),
            "age": forms.NumberInput(attrs={"class": "form-control", "placeholder": "나이 입력"}),
            "height": forms.NumberInput(attrs={"class": "form-control", "placeholder": "키 입력 (cm)"}),
            "weight": forms.NumberInput(attrs={"class": "form-control", "placeholder": "몸무게 입력 (kg)"}),
        }