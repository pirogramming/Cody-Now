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
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("이메일 주소를 반드시 입력해야 합니다.")
        if not username:
            raise ValueError("사용자 이름을 반드시 입력해야 합니다.")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
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

    # 기본 필드
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)
    nickname = models.CharField(max_length=30, unique=True, default=generate_temp_nickname)

    # 추가 프로필 정보
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=False, null=False)
    age = models.IntegerField(blank=False, null=False)
    style = models.CharField(max_length=20, choices=STYLE_CHOICES, blank=False, null=False)
    height = models.IntegerField(blank=False, null=False)
    weight = models.CharField(max_length=20, choices=WEIGHT_CHOICES, blank=False, null=False)

    # 권한 관련 필드
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # 이메일을 로그인 식별자로 사용
    REQUIRED_FIELDS = ['username']  # 추가 필수 필드

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """사용자가 특정 권한을 가지고 있는지 확인"""
        return True

    def has_module_perms(self, app_label):
        """사용자가 특정 앱의 권한을 가지고 있는지 확인"""
        return True

    @property
    def is_staff(self):
        """관리자 권한 여부"""
        return self.is_admin
