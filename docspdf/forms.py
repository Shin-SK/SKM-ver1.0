from django import forms
from .models import Quotation, QuotationItem, Invoice, InvoiceItem
from customers.models import Customer

class QuotationForm(forms.ModelForm):
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        label="顧客（会社名）",
        widget=forms.Select,
        empty_label="会社名を選択してください"
    )

    class Meta:
        model = Quotation
        fields = ['customer', 'quotation_number', 'project_name', 'contact_name', 'attention_to', 'closing_date', 'payment_due_date']
        widgets = {
            'quotation_number': forms.TextInput(attrs={'placeholder': '例: Q20230101'}),
            'project_name': forms.TextInput(attrs={'placeholder': '案件名'}),
            'contact_name': forms.TextInput(attrs={'placeholder': '担当者名'}),
            'attention_to': forms.TextInput(attrs={'placeholder': '宛先'}),
            'closing_date': forms.TextInput(attrs={'placeholder': '例: 毎月25日'}),
            'payment_due_date': forms.TextInput(attrs={'placeholder': '例: 締め日から30日後'}),
        }
        labels = {
            'customer': '顧客',
            'quotation_number': '見積書番号',
            'project_name': '案件名',  # ★追加！
            'contact_name': '担当者名',
            'attention_to': '宛先',
            'closing_date': '締め日',
            'payment_due_date': '支払期日',
        }


class QuotationItemForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=0, required=True, initial=1)
    unit_price = forms.IntegerField(min_value=0, required=True, initial=1)

    class Meta:
        model = QuotationItem
        fields = ['item_name', 'quantity', 'unit_price']
        widgets = {
            'item_name': forms.TextInput(attrs={'placeholder': '品名'}),
            'quantity': forms.NumberInput(attrs={'min': 0}),
            'unit_price': forms.NumberInput(attrs={'step': 0.01, 'min': 0}),
        }
        labels = {
            'item_name': '品名',
            'quantity': '数量',
            'unit_price': '単価',
        }


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'customer',
            'invoice_number',
            'project_name',  # ここを追加
            'contact_name',
            'attention_to',
            'closing_date',
            'payment_due_date'
        ]
        widgets = {
            'invoice_number': forms.TextInput(attrs={'placeholder': '例: INV20230101'}),
            'project_name': forms.TextInput(attrs={'placeholder': '案件名'}),
            'contact_name': forms.TextInput(attrs={'placeholder': '担当者名'}),
            'attention_to': forms.TextInput(attrs={'placeholder': '宛先'}),
            'closing_date': forms.TextInput(attrs={'placeholder': '例: 毎月25日'}),
            'payment_due_date': forms.TextInput(attrs={'placeholder': '例: 締め日から30日後'}),
        }
        labels = {
            'customer': '顧客',
            'invoice_number': '請求書番号',
            'project_name': '案件名',  # ★追加！
            'contact_name': '担当者名',
            'attention_to': '宛先',
            'closing_date': '締め日',
            'payment_due_date': '支払期日',
        }


class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['item_name', 'quantity', 'unit_price']
        widgets = {
            'item_name': forms.TextInput(attrs={'placeholder': '品名'}),
            'quantity': forms.NumberInput(attrs={'min': 1}),
            'unit_price': forms.NumberInput(attrs={'step': 0.01}),
        }
        labels = {
            'item_name': '品名',
            'quantity': '数量',
            'unit_price': '単価',
        }
