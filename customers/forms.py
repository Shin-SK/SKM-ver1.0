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


from django import forms
from .models import Customer

COMPANY_CHOICES = [
    ('株式会社', '株式会社'),
    ('有限会社', '有限会社'),
    ('合同会社', '合同会社'),
    ('', 'なし'),
]

class CustomerForm(forms.ModelForm):
    company_prefix = forms.ChoiceField(
        choices=COMPANY_CHOICES,
        label="会社種別",
        required=False
    )
    company_suffix = forms.CharField(
        label="会社名（その他）",
        required=False
    )

    class Meta:
        model = Customer
        # company_name はフォーム上では直接扱わず、内部で生成する
        fields = ['company_prefix', 'company_suffix', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'logo']

    def clean(self):
        cleaned_data = super().clean()
        prefix = cleaned_data.get('company_prefix', '')
        suffix = cleaned_data.get('company_suffix', '')
        # 連結して company_name にセット
        cleaned_data['company_name'] = prefix + suffix
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.company_name = self.cleaned_data.get('company_name', '')
        if commit:
            instance.save()
        return instance
