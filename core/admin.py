from django.contrib import admin
from django import forms
from .models import CompanyProfile

class CompanyProfileAdminForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['name', 'logo', 'seal', 'address', 'phone', 'email', 'contact_person', 'bank_details']

@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    form = CompanyProfileAdminForm
    list_display = ['name', 'phone', 'email', 'address']
