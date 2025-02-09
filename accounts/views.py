from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import Profile

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # メール認証後に有効化
            user.save()

            # プロフィールを作成
            Profile.objects.create(user=user)
            
            # トークンとUIDを生成
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activation_link = f"http://127.0.0.1:8000/activate/{uid}/{token}/"
            
            # 認証メールを送信
            send_mail(
                'アカウント認証',
                f'以下のリンクをクリックしてアカウントを認証してください: {activation_link}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return render(request, 'accounts/signup_email_sent.html')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'accounts/activation_success.html')  # 認証成功画面
    else:
        return render(request, 'accounts/activation_invalid.html')  # 認証失敗画面


@login_required
def edit_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)  # プロフィールを取得、存在しない場合は作成

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=user)  # ユーザー情報をバインド
        if form.is_valid():
            form.save()  # ユーザー情報を保存
            # プロフィールの追加フィールドを手動で保存
            profile.department = form.cleaned_data.get('department')
            profile.phone_number = form.cleaned_data.get('phone_number')
            profile.save()
            return redirect('mypage')  # 保存後はマイページへリダイレクト
    else:
        # 初期データとしてプロフィールのフィールドをセット
        form = ProfileUpdateForm(instance=user, initial={
            'department': profile.department,
            'phone_number': profile.phone_number,
        })

    return render(request, 'accounts/edit_profile.html', {'form': form})