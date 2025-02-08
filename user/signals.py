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
    if created and instance.email:  # 새롭게 생성된 사용자만 처리
        subject = "[CodyNow] 회원가입을 축하합니다!"
        html_message = """
<html>
  <head>
    <meta charset="utf-8">
    <style>
      body {
        font-family: Arial, sans-serif;
        background-color: #f5f5f5;
        padding: 20px;
      }
      .container {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 5px;
        box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
      }
      h1 {
        color: #333333;
      }
      p {
        color: #666666;
        line-height: 1.6;
      }
      .footer {
        margin-top: 20px;
        font-size: 0.9em;
        color: #999999;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>안녕하세요, CodyNow 입니다!</h1>
      <p>
        나만의 Ai 스타일 에이전트 <strong>CodyNow</strong>에 가입해주셔서 감사합니다.<br>
        회원가입이 성공적으로 완료되었습니다!<br>
        이제 다양한 스타일 추천과 맞춤형 코디 서비스를 즐길 수 있습니다.
      </p>
      <p>
        💡 궁금한 점이 있다면 언제든지 문의해주세요!<br>
        📩 고객센터: <a href="mailto:codynoww@gmail.com">codynoww@gmail.com</a>
      </p>
      <p class="footer">CodyNow 팀 드림.</p>
    </div>
  </body>
</html>
"""
        from_email = "noreply@yourwebsite.com"  # 발신 이메일 (SMTP 설정 필요)
        recipient_list = [instance.email]

        # 일반 텍스트 메시지와 HTML 메시지를 모두 전달할 수 있습니다.
        # 만약 일반 텍스트 메시지가 필요하지 않다면 빈 문자열("")로 설정하세요.
        send_mail(
            subject,
            "",  # 일반 텍스트 메시지 (필수 인자)
            from_email,
            recipient_list,
            fail_silently=False,
            html_message=html_message,  # HTML 형식 메시지 전달
        )