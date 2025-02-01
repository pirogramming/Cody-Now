from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from uuid import uuid4  # 랜덤 닉네임 생성용
from django.core.validators import MaxLengthValidator

def generate_temp_nickname():
    return f"user_{uuid4().hex[:8]}"  # 예: user_a1b2c3d4

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        """
        일반 사용자 생성 메서드
        """
        if not email:
            raise ValueError("이메일을 입력해주세요")
        
        email = self.normalize_email(email)

        # username이 제공되지 않으면 자동 생성
        if not username:
            username = email.split('@')[0]  # 예: "test@example.com" -> "test"
        
        extra_fields.setdefault("nickname", generate_temp_nickname())  # 기본 닉네임 자동 생성

        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        """
        슈퍼유저 생성 메서드 (is_superuser, is_staff=True 설정 필수)
        """
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    사용자 모델 (이메일 기반 로그인)
    """
    GENDER_CHOICES = [
        ("M", "남성"),
        ("F", "여성"),
        ("O", "기타"),
    ]

    STYLE_CHOICES = [
        ("casual", "캐주얼"),
        ("formal", "포멀"),
        ("sporty", "스포티"),
        ("street", "스트릿"),
    ]

    WEIGHT_CHOICES = [
        ("under_50", "50kg 미만"),
        ("50_60", "50kg ~ 60kg"),
        ("60_70", "60kg ~ 70kg"),
        ("over_70", "70kg 이상"),
    ]

    # 필수 필드
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True, blank=True, null=True)
    nickname = models.CharField(max_length=30, unique=True, default=generate_temp_nickname)

    # 추가 프로필 정보
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    style = models.CharField(max_length=20, choices=STYLE_CHOICES, blank=True, null=True, validators=[MaxLengthValidator(20)])
    height = models.IntegerField(blank=True, null=True)
    weight = models.CharField(max_length=20, choices=WEIGHT_CHOICES, blank=True, null=True)

    # 권한 관련 필드
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # ✅ Django 관리자 여부
    is_superuser = models.BooleanField(default=False)  # ✅ 슈퍼유저 여부

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # 이메일을 로그인 식별자로 사용
    REQUIRED_FIELDS = ["username"]  # 추가 필수 필드

    def __str__(self):
        return self.email