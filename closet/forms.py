from django import forms
from .models import Outfit
from django.utils.text import get_valid_filename

class OutfitForm(forms.ModelForm):
    class Meta:
        model = Outfit
        fields = ['image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            image.name = get_valid_filename(image.name)
        return image
