from django import forms
from .models import Outfit,UserCategory
from django.utils.text import get_valid_filename

class OutfitForm(forms.ModelForm):
    user_category = forms.ModelChoiceField(
        queryset=UserCategory.objects.all(),
        required=False,
        empty_label="사용자 지정 카테고리 (선택)",
        label="사용자 추가 카테고리"
    )
      
    class Meta:
        model = Outfit
        fields = ['image','user_category']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            image.name = get_valid_filename(image.name)
        return image
