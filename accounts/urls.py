from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),  # ログイン
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),  # ログアウト
    path('signup/', views.signup, name='signup'),  # サインアップ
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate_account'),  # アカウント認証
]
