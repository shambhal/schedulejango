from django import forms

class ConfigForm1(forms.Form):
    fb_id = forms.CharField(label="Facebook ID",widget=forms.widgets.TextInput(attrs={"class": "form-control",}), required=False)
    gci_id = forms.CharField(label="Google Login ID", required=False)
    x_id = forms.CharField(label="X ID", required=False)
    instagram_id=forms.CharField(label="Instagram Id",required=False)

class ConfigBasic(forms.Form):
    support_email = forms.CharField(label="Support Email", widget=forms.widgets.TextInput(attrs={"class": "form-control",}),required=False)    
    mmode = forms.ChoiceField(label="Maintenance Mode", widget=forms.Select(attrs={
            'class': 'form-control'
        }), required=True,initial=True,choices=[(1,True),(0,False)])
   