from .base import *
import os

print('production 실행')

DEBUG = False

ALLOWED_HOSTS = [
    "codynow.com",
    "www.codynow.com",
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

# 캐시 설정
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': env('REDIS_URL'),
    }
}

# 로그 디렉토리 생성
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)  # logs 디렉토리가 없으면 생성

# 로깅 설정
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'django.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# # 정적 파일 설정
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # STATICFILES_DIRS와 다른 경로 사용
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# # production 환경에서는 STATICFILES_DIRS 재정의
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]
