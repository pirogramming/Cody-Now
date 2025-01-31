from .base import *

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# 개발 환경 특화 설정
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # 개발 시 이메일을 콘솔에 출력

# 개발 도구
INSTALLED_APPS += ['debug_toolbar']

# Debug Toolbar 미들웨어 설정 수정
MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE

# Debug Toolbar 설정
INTERNAL_IPS = ["127.0.0.1"]
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True,
}

