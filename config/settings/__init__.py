import os

ENVIRONMENT = os.getenv("DJANGO_ENV", "local")

# base.py의 설정을 먼저 로드
from .base import *

# 환경별 설정 로드
if ENVIRONMENT == "production":
    from .production import *
else:
    from .local import *

# settings 패키지 초기화