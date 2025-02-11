from config.settings import serv_settings, BASE_DIR  # __init__.py에서 가져오기
from .base import *

print('local 실행')

DEBUG = True
ALLOWED_HOSTS = ["*"]

# 개발 환경 특화 설정
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = serv_settings('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = serv_settings('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# URL prefix for static files
STATIC_URL = '/static/'

# 개발 환경에서 사용할 정적 파일 디렉토리 목록
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# collectstatic 명령어로 정적 파일이 모이는 경로
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 정적 파일 찾을 앱 목록
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 기본 MIDDLEWARE 설정 유지
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