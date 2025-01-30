from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """
    소셜 회원가입이 완료되면 자동으로 환영 이메일을 보냄.
    """
    if created and instance.email:  # ✅ 새롭게 생성된 사용자만 처리
        subject = "[CodyNow] 회원가입을 축하합니다! 🎉"
        message = f"""
안녕하세요, CodyNow 입니다!

나만의 Ai 스타일 에이전트 CodyNow에 가입해주셔서 감사합니다. 
회원가입이 성공적으로 완료되었습니다!
이제 다양한 스타일 추천과 맞춤형 코디 서비스를 즐길 수 있습니다.

💡 궁금한 점이 있다면 언제든지 문의해주세요!
📩 고객센터: codynoww@gmail.com

CodyNow 팀 드림.
"""
        from_email = "noreply@yourwebsite.com"  # 발신 이메일 (SMTP 설정 필요)
        recipient_list = [instance.email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)