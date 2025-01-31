import os
import environ
from pathlib import Path


print("init 실행")

# settings 디렉토리 기준 BASE_DIR
SETTINGS_DIR = Path(__file__).resolve().parent
BASE_DIR = SETTINGS_DIR.parent.parent  # config/ 디렉토리 기준

env = environ.Env()
# 최상위 프로젝트 경로의 .env 읽기
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# 환경 변수에서 DJANGO_ENV 가져오기 (기본값 local)
ENVIRONMENT = env("DEPLOY_ENV")

# print(ENVIRONMENT)

# 1) 공통 설정 불러오기
from .base import *

# 2) production 이면 production.py, 아니면 local.py
if ENVIRONMENT == "production":
    from .production import *
else:
    from .local import *