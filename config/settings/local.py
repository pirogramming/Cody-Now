from .base import *

# print('local 실행')

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# 개발 환경 특화 설정
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # 개발 시 이메일을 콘솔에 출력

# 개발 도구
INSTALLED_APPS += ['debug_toolbar']

# MIDDLEWARE 전체 재정의
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# Debug Toolbar 설정
INTERNAL_IPS = ["127.0.0.1"]
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True,
}

# 이메일 설정 
load_dotenv()  # .env 파일 로드

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER