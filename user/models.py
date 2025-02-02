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

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUser(AbstractBaseUser, PermissionsMixin):
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

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True, blank=True, null=True)
    nickname = models.CharField(max_length=30, unique=True)

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
        null=True
    )
    
    age = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)

    style = models.CharField(
        max_length=20,
        choices=[(key, value) for key, value in STYLE_CHOICES],  # ✅ 빈 값 제거
        blank=False,  # ✅ 빈 값 허용 X
        null=False,  # ✅ NULL 허용 X
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = BaseUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email