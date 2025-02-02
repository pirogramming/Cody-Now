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
        ("M", "남성"),
        ("F", "여성"),
    ]
    STYLE_CHOICES = [
        ("noidea", "잘 모르겠어요"),
        ("casual", "캐주얼"),
        ("formal", "포멀"),
        ("sporty", "스포티"),
        ("street", "스트릿"),
    ]

    # RadioSelect에 attrs={'required': True} 추가
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect(attrs={'required': True}),
        required=True,
    )
    # style도 동일하게
    style = forms.ChoiceField(
        choices=STYLE_CHOICES,
        widget=forms.RadioSelect(attrs={'required': True}),
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ["nickname", "gender", "age", "height", "weight", "style"]
        widgets = {
            "nickname": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "닉네임 입력",
                "required": True
            }),
            "age": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "나이 입력",
                "required": True
            }),
            "height": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "키 입력 (cm)",
                "required": True
            }),
            "weight": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "몸무게 입력 (kg)",
                "required": True
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 만약 "noidea"를 기본값으로 지정하고 싶다면 아래처럼 설정
        # (단, 이 경우 이미 'noidea'가 선택되어 있어
        # 브라우저가 '필수 입력'으로 막지는 않습니다.)

    def clean_style(self):
        style = self.cleaned_data.get("style")
        if style not in dict(self.STYLE_CHOICES):
            raise forms.ValidationError("스타일을 선택해야 합니다.")
        return style