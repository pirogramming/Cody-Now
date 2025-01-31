import os
import environ
from pathlib import Path


print("init 실행")

# 최상위 디렉토리 기준 BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# environ 설정
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# 환경 변수에서 DEPLOY_ENV 가져오기 (기본값 local)
ENVIRONMENT = env('DEPLOY_ENV')  # os.getenv 대신 env() 사용

print(f"Current environment: {ENVIRONMENT}")

print("ENV file path:", os.path.join(BASE_DIR, '.env'))
print("Raw env value:", env('DEPLOY_ENV'))

# 1) 공통 설정 불러오기
from .base import *

# 2) production 이면 production.py, 아니면 local.py
if ENVIRONMENT == "production":
    from .production import *
else:
    from .local import *


