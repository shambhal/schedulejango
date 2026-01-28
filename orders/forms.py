from django import forms
from .models import Order
from datetime import timedelta
from django.utils import timezone
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["status"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            seven_days_ago = timezone.now() - timedelta(days=7)

            if self.instance.updated_at< seven_days_ago:

                #self.fields['status'].disabled = True
                self.fields['status'].choices=[('EXPIRED',"Expired")]