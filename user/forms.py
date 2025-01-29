from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import CustomUser

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
        label="Email"
    )
class SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        # help_text='150자 이하 문자, 숫자 그리고 @/./+/-/_만 가능합니다.'
    )
    email = forms.EmailField(
        max_length=255,
        help_text='유효한 이메일 주소를 입력하세요.'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        help_text='최소 8자 이상의 비밀번호를 입력하십시오'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        help_text='같은 비밀번호를 한번 더 입력하십시오'
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["nickname", "gender", "age", "style", "height", "weight"]
        widgets = {
            "gender": forms.RadioSelect(choices=CustomUser.GENDER_CHOICES),
            "style": forms.RadioSelect(choices=CustomUser.STYLE_CHOICES),
            "weight": forms.RadioSelect(choices=CustomUser.WEIGHT_CHOICES),
        }

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["nickname", "gender", "age", "height", "weight"]
        widgets = {
            "gender": forms.RadioSelect(choices=CustomUser.GENDER_CHOICES),
            "weight": forms.RadioSelect(choices=CustomUser.WEIGHT_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True  # ✅ 모든 필드를 필수 입력으로 설정
