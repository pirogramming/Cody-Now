"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# 이전 설정으로 복원
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # .production 제거

application = get_wsgi_application()
