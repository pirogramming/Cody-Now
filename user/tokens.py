from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from datetime import datetime, timedelta, timezone

class ExpiringPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    """
    5분 후 만료되는 비밀번호 재설정 토큰 생성
    """
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        )

    def check_token(self, user, token):
        """
        토큰이 유효한지 확인하고, 5분이 지났다면 만료 처리
        """
        if not super().check_token(user, token):
            return False  # 기본 토큰 검증 실패

        try:
            timestamp = int(token.split("-")[-1])  # 토큰에서 타임스탬프 가져오기
            token_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)  # ✅ 변경된 코드
            current_time = datetime.now(timezone.utc)  # ✅ 변경된 코드

            if current_time - token_time > timedelta(minutes=1):  # ✅ 1분 만료 설정
                return False  # 1분 초과 시 토큰 만료
        except Exception:
            return False  # 오류 발생 시 토큰 무효화

        return True  # 유효한 경우만 True 반환

# ✅ 전역 변수로 토큰 생성기 인스턴스화
password_reset_token_generator = ExpiringPasswordResetTokenGenerator()