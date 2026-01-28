from django import forms
from .models import Doctor
from django.utils.translation import gettext_lazy as _


class DoctorForm1(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ["email", "phone", "gender"]

    name = forms.CharField(
        label=_("Name"),
        widget=forms.widgets.TextInput(attrs={"class": "form-control"}),
        required=True,
    )

    def save(self, commit=True):
        name = self.cleaned_data.pop("name", "")
        first_name, last_name = self._split_name(name)

        # Update the instance
        self.instance.first_name = first_name
        self.instance.last_name = last_name

        return super().save(commit=commit)

    def _split_name(self, name):
        parts = name.strip().split(" ", 1)
        first = parts[0]
        last = parts[1] if len(parts) > 1 else ""
        return first, last

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields[
                "name"
            ].initial = f"{self.instance.first_name} {self.instance.last_name}"


class DoctorPForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            "license_number",
            "specialization",
            "years_of_experience",
            "qualification",
            "bio",
        ]


class DoctorTimingsForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            "categories",
            "sunday",
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "slot",
            "off",
        ]
