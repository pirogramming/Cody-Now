from django import forms
from .models import Outfit

class OutfitForm(forms.ModelForm):
    class Meta:
        model = Outfit
        fields = '__all__' 
