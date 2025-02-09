from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='メールアドレス')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        label='姓', 
        max_length=30, 
        required=False
    )
    last_name = forms.CharField(
        label='名', 
        max_length=30, 
        required=False
    )
    email = forms.EmailField(
        label='メールアドレス', 
        required=True
    )
    username = forms.CharField(
        label='ログインID', 
        max_length=150, 
        required=True
    )
    department = forms.CharField(
        label='部署',
        max_length=100,
        required=False
    )
    phone_number = forms.CharField(
        label='電話番号',
        max_length=15,
        required=False
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'department', 'phone_number']
