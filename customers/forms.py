# customers/forms.py
from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'company_name', 'address']
        widgets = {
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'email': forms.EmailInput(),
            'phone_number': forms.TextInput(),
            'company_name': forms.TextInput(),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class CustomerCSVImportForm(forms.Form):
    file = forms.FileField(label="CSVファイル")
