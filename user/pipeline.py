# user/pipeline.py
from django.contrib.auth import get_user_model

def associate_by_email(strategy, details, user=None, *args, **kwargs):
    """
    OAuth 로그인 시, 이메일을 기준으로 기존 사용자가 있다면 연결(merge)합니다.
    만약 user가 이미 있으면 아무 작업도 하지 않습니다.
    """
    if user:
        # 이미 로그인된 사용자면 추가 작업이 필요없으므로 그대로 반환
        return {'user': user}

    email = details.get('email')
    if not email:
        # 이메일 정보가 없으면 더 이상 연결할 수 없으므로 pass
        return

    User = get_user_model()
    try:
        # 이메일을 기준으로 기존 사용자 검색
        existing_user = User.objects.get(email=email)
        return {'user': existing_user}
    except User.DoesNotExist:
        # 기존에 해당 이메일 사용자가 없다면, 그대로 진행
        return
'''
#settings.py에 추가해야 함

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    
    # 여기서 이메일 기반 연결을 시도합니다.
    'user.pipeline.associate_by_email',  # user 앱 내부에 작성한 함수

    # 만약 기존 사용자와 연결되지 않았다면 새로 생성합니다.
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)
'''