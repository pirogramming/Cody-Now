from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from uuid import uuid4  # 랜덤 문자열 생성을 위한 라이브러리

def generate_temp_nickname():
    return f"user_{uuid4().hex[:8]}"  # 예: user_a1b2c3d4

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and returns a user with an email and username.
        """
        if not email:
            raise ValueError('이메일을 입력해주세요')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """
        Creates and returns a superuser with an email and username.
        """
        user = self.create_user(email=email, username=username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        이메일만으로 유저 생성 (아이디 제거)
        """
        if not email:
            raise ValueError("이메일을 입력해야 합니다.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        이메일만으로 관리자 계정 생성 (아이디 제거)
        """
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        ("M", "남성"),
        ("F", "여성"),
        ("O", "기타"),
    ]

    WEIGHT_CHOICES = [
        ("under_50", "50kg 미만"),
        ("50_60", "50kg ~ 60kg"),
        ("60_70", "60kg ~ 70kg"),
        ("over_70", "70kg 이상"),
    ]

    # 기본 필드
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=30, unique=True, blank=True, null=True)

    # 추가 프로필 정보
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    weight = models.CharField(max_length=20, choices=WEIGHT_CHOICES, blank=True, null=True)

    # 권한 관련 필드
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"  # ✅ 이메일을 로그인 식별자로 사용
    REQUIRED_FIELDS = []  # ✅ username 제거

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        """관리자 권한 여부"""
        return self.is_admin