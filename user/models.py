from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from uuid import uuid4  # 랜덤 닉네임 생성용
from django.core.validators import MaxLengthValidator

def generate_temp_nickname():
    return f"user_{uuid4().hex[:8]}"  # 예: user_a1b2c3d4



def generate_temp_nickname():
    return f"user_{uuid4().hex[:8]}"  # 예: user_a1b2c3d4

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        일반 사용자 생성 메서드 - 이메일을 기준으로 구분, 닉네임 중복 허용
        """
        if not email:
            raise ValueError("이메일을 입력해주세요")

        email = self.normalize_email(email)

        # 이메일로 기존 사용자 확인 (이미 존재하면 반환)
        existing_user = self.model.objects.filter(email=email).first()
        if existing_user:
            return existing_user

        # username 자동 생성 (이메일 앞부분 사용)
        if not extra_fields.get("nickname"):
            extra_fields["nickname"] = generate_temp_nickname(email)  
        
        # 닉네임 중복 허용 (unique 제거)
        extra_fields.setdefault("nickname", generate_temp_nickname())

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        슈퍼유저 생성 메서드 (이메일로 사용자 구분, 닉네임 중복 허용)
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email=email, password=password, **extra_fields)

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
    nickname = models.CharField(max_length=30, blank=False, null=False) 

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
        default="noidea"
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email