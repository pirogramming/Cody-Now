# from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
# from allauth.account.utils import user_field
# from django.shortcuts import redirect

# class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
#     def populate_user(self, request, sociallogin, data):
#         """
#         소셜 로그인 시, 기본 사용자 데이터를 설정하는 메서드.
#         """
#         user = super().populate_user(request, sociallogin, data)

#         # 추가적으로 user 모델에 저장할 필드
#         user.nickname = data.get("nickname", "")
#         user.gender = data.get("gender", None)
#         user.age = data.get("age", None)
#         user.height = data.get("height", None)
#         user.weight = data.get("weight", None)

#         return user

#     def save_user(self, request, sociallogin, form=None):
#         """
#         소셜 회원가입 시 추가 필드를 저장하도록 수정.
#         """
#         user = sociallogin.user

#         # 폼에서 데이터 가져오기
#         user.nickname = request.POST.get("nickname", "")
#         user.gender = request.POST.get("gender", None)
#         user.age = request.POST.get("age", None)
#         user.height = request.POST.get("height", None)
#         user.weight = request.POST.get("weight", None)

#         user.save()
#         return user