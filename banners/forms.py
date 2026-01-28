from django import forms
from .models import Banner
from django.utils.translation import gettext_lazy as _

class BannerForm1(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ["category","sort_order","tag"]

    