from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CompanyProfile
from .forms import CompanyProfileForm
from django.core.mail import send_mail
from core.utils import get_sender_email

# 管理者専用デコレーター
def admin_required(user):
    return user.is_staff


def send_test_email():
    """テストメールを送信"""
    send_mail(
        'テストメールの件名',
        'このメールはDjangoから送信されました。',
        get_sender_email(),  # ここで動的に取得！
        ['user@example.com'],
        fail_silently=False,
    )
