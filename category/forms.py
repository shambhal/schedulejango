from django import forms
from models import Category
from django.utils.translation import gettext_lazy as _


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["email", "phone", "gender"]
        name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Name"}))
