from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),  # ログイン
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),  # ログアウト
    path('signup/', views.signup, name='signup'),  # サインアップ
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate_account'),  # アカウント認証
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
