from django import forms
from .models import InventoryItem

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['product_name', 'stock_count', 'product_code', 'notes', 'image']
        widgets = {
            'product_name': forms.TextInput(),
            'stock_count': forms.NumberInput(),
            'product_code': forms.TextInput(),
            'notes': forms.Textarea(),
            'image': forms.ClearableFileInput(),
        }

class InventoryCSVImportForm(forms.Form):
    csv_file = forms.FileField(label="CSVファイルを選択")
