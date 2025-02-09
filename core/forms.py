from django import forms
from .models import CompanyProfile

class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['name', 'logo', 'seal', 'address', 'phone', 'email', 'contact_person', 'closing_date', 'payment_due_date']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'closing_date': forms.TextInput(attrs={'placeholder': '例: 毎月25日'}),
            'payment_due_date': forms.TextInput(attrs={'placeholder': '例: 締め日から30日後'}),
        }
        labels = {
            'name': '会社名',
            'logo': '会社ロゴ',
            'seal': '会社印鑑',  # 追加
            'address': '住所',
            'phone': '電話番号',
            'email': 'メールアドレス',
            'contact_person': '担当者名',
            'closing_date': '締め日',
            'payment_due_date': '支払期日',
        }
