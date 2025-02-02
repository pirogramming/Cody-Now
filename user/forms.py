from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import CustomUser

class CustomAuthenticationForm(AuthenticationForm):
    """
    로그인 폼 - 이메일을 아이디처럼 사용
    """

class SignUpForm(UserCreationForm):
    """
    회원가입 폼 - 이메일과 비밀번호만 입력받도록 변경
    """

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

    age = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "나이 입력"}),
        required=True
    )

    height = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "키 입력 (cm)"}),
        required=True
    )

    weight = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "몸무게 입력 (kg)"}),
        required=True
    )

    style = forms.ChoiceField(
        choices=STYLE_CHOICES, 
        widget=forms.Select(),
        required=True
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