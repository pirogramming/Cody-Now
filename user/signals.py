from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """
    회원가입이 완료되면 자동으로 환영 이메일을 보냄.
    """
    if created and instance.email:  # ✅ 새롭게 생성된 사용자만 처리
        subject = "🎉 회원가입을 축하합니다!"
        message = f"안녕하세요, {instance.nickname}님!\n\n회원가입을 성공적으로 완료하셨습니다.\n즐거운 쇼핑 되세요! 😊"
        from_email = "noreply@yourwebsite.com"
        recipient_list = [instance.email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)