"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
import environ
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
# BASE_DIR를 이용해서 .env 파일 경로 지정
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# 구글 OAuth2 키와 시크릿 가져오기
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

# OAuth 후 리디렉션 URL 설정
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = 'http://127.0.0.1:8000/complete/google/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/profile/'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-w&9&6-j4%a!6mk^n%1975k*#ew_3irr%j$6bcx+5g$_7#o#x9*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'social_django',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'user',
    'closet',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.kakao',
    'allauth.socialaccount.providers.naver',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends', #social 로그인 관련 template 추가부분
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='5432'),
        'OPTIONS': {
            'client_encoding': 'UTF8',
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
# 240116 - 아무거나 입력해도 회원가입 가능하도록 수정
AUTH_USER_MODEL = 'user.CustomUser'

AUTH_PASSWORD_VALIDATORS = [

]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',  # Google OAuth2 백엔드 추가
    'django.contrib.auth.backends.ModelBackend',  # 기본 Django 인증 백엔드

    'allauth.account.auth_backends.AuthenticationBackend',
)


SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    
    # 여기서 이메일 기반 연결을 시도합니다.
    'user.pipeline.associate_by_email',  # user 앱 내부에 작성한 함수

    # 만약 기존 사용자와 연결되지 않았다면 새로 생성합니다.
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

#보안 관련 설정
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]

LOGIN_URL = 'user:login'
LOGIN_REDIRECT_URL = 'closet:dashboard'
LOGOUT_REDIRECT_URL = 'user:login'

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# 추가할 부분
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# 배포 시 필요한 설정 (선택사항)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'closet:dashboard'


# media
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') 

#input api
from dotenv import load_dotenv

load_dotenv()

INPUT_API_KEY = os.getenv("INPUT_API_KEY")

SITE_ID = 1

SOCIALACCOUNT_LOGIN_ON_GET = True
LOGIN_REDIRECT_URL = 'closet:dashboard'
ACCOUNT_LOGOUT_REDIRECT_URL = 'closet:dashboard'
ACCOUNT_LOGOUT_ON_GET = True 

ACCOUNT_ADAPTER = "user.account_adapter.CustomAccountAdapter"
SOCIALACCOUNT_ADAPTER = "user.account_adapter.CustomSocialAccountAdapter"

ACCOUNT_FORMS = {
    "socialsignup": "user.forms.SocialSignupForm",
    
}

ACCOUNT_SIGNUP_REDIRECT_URL = "/profile/" 
SOCIALACCOUNT_SIGNUP_REDIRECT_URL = "/profile/"

# 이메일 설정 
load_dotenv()  # .env 파일 로드

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_SIGNUP_REDIRECT_URL = "/profile/"
SOCIALACCOUNT_SIGNUP_REDIRECT_URL = "/profile/"
ACCOUNT_ADAPTER = "user.account_adapter.CustomAccountAdapter"
ACCOUNT_SESSION_REMEMBER = False

OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
print(OPENWEATHER_API_KEY)
