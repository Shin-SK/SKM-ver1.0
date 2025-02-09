from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CompanyProfile
from .forms import CompanyProfileForm

# 管理者専用デコレーター
def admin_required(user):
    return user.is_staff
