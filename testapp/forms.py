from django import forms
from django.forms import fields
from .models import UserProfile

class PhotoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['photo']