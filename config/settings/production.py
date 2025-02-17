from config.settings import serv_settings, BASE_DIR  # __init__.py에서 가져오기
from .base import *
import os

print('production 실행')

DEBUG = False
os.environ['DEBUG'] = 'False'  # 환경변수도 강제로 설정

# 디버그 관련 설정들도 추가
TEMPLATE_DEBUG = False
VIEW_DEBUG = False

# 에러 핸들링 설정 추가
ADMINS = [('Your Name', 'your-email@example.com')]
MANAGERS = ADMINS

# 500 에러 템플릿 확인
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
            ],
            'debug': False,  # 템플릿 디버그도 비활성화
        },
    },
]

ALLOWED_HOSTS = [
    "codynow.com",
    "www.codynow.com",

]


CSRF_TRUSTED_ORIGINS = [
    'https://www.codynow.com',  # 도메인 추가
    'http://www.codynow.com',  # HTTP 요청도 허용
    'https://codynow.com',  # 도메인 추가
    'http://codynow.com',  # HTTP 요청도 허용
]

# 보안 설정 (일시적으로 비활성화)
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# 이메일 설정
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = serv_settings('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = serv_settings('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# 캐시 설정
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': serv_settings('REDIS_URL'),
    }
}

# 로그 디렉토리 생성
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)  # logs 디렉토리가 없으면 생성

# 로깅 설정
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',  # ERROR에서 INFO로 변경
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'django.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'closet': {  # 앱 이름
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"

# Static files
# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# # 정적 파일 설정
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # STATICFILES_DIRS와 다른 경로 사용
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# # production 환경에서는 STATICFILES_DIRS 재정의
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]
WSGI_APPLICATION = "myproject.wsgi.application"


print(f'Current DEBUG setting: {DEBUG}')

GOOGLE_SEARCH_API_KEY = serv_settings('GOOGLE_SEARCH_API_KEY')