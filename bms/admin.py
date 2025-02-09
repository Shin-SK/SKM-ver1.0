from django.contrib import admin
from .models import Employee
from django.utils.safestring import mark_safe
from django import forms
from .models import Product

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email', 'department', 'employee_number')
    search_fields = ('last_name', 'first_name', 'email', 'department', 'employee_number')
    list_filter = ('department',)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    class Media:
        js = ('admin/custom_fields.js',)  # Vue.jsのスクリプトを読み込む

class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ('name', 'price', 'stock')

    def custom_fields_display(self, obj):
        return mark_safe(f'<div id="custom-fields-container" data-fields=\'{obj.custom_fields}\'></div>')

    custom_fields_display.short_description = "カスタムフィールド"
    readonly_fields = ('custom_fields_display',)

admin.site.register(Product, ProductAdmin)
