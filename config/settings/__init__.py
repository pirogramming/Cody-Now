import os
from pathlib import Path
import dotenv

# 최상위 디렉토리 기준 BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# .env 파일 경로 설정 및 로드
ENV_PATH = os.path.join(BASE_DIR, '.env')

# dotenv 로드
if os.path.exists(ENV_PATH):
    dotenv.load_dotenv(ENV_PATH, override=True)

def serv_settings(key, default=None):
    value = os.getenv(key, default)
    return value

# 환경 변수에서 DEPLOY_ENV 가져오기
ENVIRONMENT = serv_settings('DEPLOY_ENV', 'local')

# 1) 공통 설정 불러오기
from .base import *

# 2) production 이면 production.py, 아니면 local.py
if ENVIRONMENT == "production":
    from .production import *
else:
    from .local import *


