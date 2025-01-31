import os

ENVIRONMENT = os.getenv("DJANGO_ENV", "local")

if ENVIRONMENT == "production":
    from .production import *
else:
    from .local import *

from .base import *

# settings 패키지 초기화