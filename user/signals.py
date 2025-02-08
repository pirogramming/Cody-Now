from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
import os

User = get_user_model()

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """
    사용자가 회원가입하면 자동으로 환영 이메일을 보냄.
    """
    if created and instance.email:  # 새로 생성된 사용자만 처리
        subject = "[CodyNow] 회원가입을 축하합니다!"
        from_email = "noreply@yourwebsite.com"
        recipient_list = [instance.email]

        # HTML 메시지에서 CID를 사용하여 이미지 삽입
        html_message = """\
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body { font-family: Arial, sans-serif; text-align: center; background: #f5f5f5; padding: 20px; }
                .container { background: #ffffff; padding: 20px; border-radius: 5px; text-align: center; }
                h1 { color: #333; }
                .button { display: inline-block; background: #000000; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
            </style>
        </head>
        <body>
            <div class="container">
                <img src="cid:banner_image" width="100%" alt="CodyNow Banner">
                <h1>안녕하세요, CodyNow 입니다!</h1>
                <h3>회원가입을 축하드립니다!</h3>
                <a href="https://codynow.com" class="button">CodyNow 바로가기</a>
                <p>고객센터: <a href="mailto:codynoww@gmail.com">codynoww@gmail.com</a></p>
            </div>
        </body>
        </html>
        """

        # Email 객체 생성
        email = EmailMultiAlternatives(subject, "", from_email, recipient_list)
        email.attach_alternative(html_message, "text/html")

        # **올바른 이미지 경로 반영**
        image_path = os.path.join("static/images/email-banner.jpeg")
        
        if os.path.exists(image_path):  # 이미지 파일 존재 확인
            with open(image_path, "rb") as img:
                email.attach("email-banner.jpeg", img.read(), "image/jpeg")
            
            email.content_subtype = "html"
            email.mixed_subtype = "related"

            # 이미지 CID(Content-ID) 설정
            email.attachments[-1]["Content-ID"] = "<banner_image>"
            email.attachments[-1]["Content-Disposition"] = "inline"

        email.send()