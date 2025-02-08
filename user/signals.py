import os
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from email.mime.image import MIMEImage

User = get_user_model()

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """
    소셜 회원가입이 완료되면 자동으로 환영 이메일을 보냄.
    """
    if created and instance.email:  # 새롭게 생성된 사용자만 처리
        subject = "[CodyNow] 회원가입을 축하합니다!"
        from_email = "noreply@yourwebsite.com"  # 발신 이메일 (SMTP 설정 필요)
        recipient_list = [instance.email]

        # 이메일 본문 (HTML)
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
        text-align: center;
      }
      h1 {
        color: #333333;
      }
      h3 {
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
      .button {
        display: inline-block;
        padding: 10px 20px;
        margin: 20px 0;
        background-color: #000000;
        color: #ffffff;
        text-decoration: none;
        border-radius: 5px;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <img src="cid:email_banner" alt="CodyNow Banner" style="width: 100%; max-width: 600px;">
      <h1>안녕하세요,<br>CodyNow 입니다!</h1>
      <h3>
        나만의 Ai 스타일 에이전트<br><strong>CodyNow</strong>에 가입해주셔서 감사합니다.<br>
        <br>
        이제 맞춤형 스타일 추천과<br> 코디 서비스를 이용하실 수 있습니다.
      </h3>
      <a href="https://codynow.com" class="button">CodyNow 바로가기</a>
      <p>
        고객센터: <a href="mailto:codynoww@gmail.com">codynoww@gmail.com</a>
      </p>
      <p class="footer">CodyNow 팀 드림.</p>
    </div>
  </body>
</html>
"""

        # 이메일 객체 생성
        email = EmailMultiAlternatives(subject, "", from_email, recipient_list)
        email.attach_alternative(html_message, "text/html")

        # 이메일에 이미지 첨부 (로컬 파일 읽기)
        static_image_path = os.path.join(settings.BASE_DIR, "static/images/email-banner.jpeg")
        if os.path.exists(static_image_path):  # 파일이 존재하는지 확인
            with open(static_image_path, "rb") as img:
                image = MIMEImage(img.read())
                image.add_header("Content-ID", "<email_banner>")
                image.add_header("Content-Disposition", "inline", filename="email-banner.jpeg")
                email.attach(image)

        # 이메일 전송
        email.send()