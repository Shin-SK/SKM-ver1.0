from django.urls import path, include
from . import views
from django.contrib import admin  # adminをインポート
from accounts import views as accounts_views  # アカウント用のビューをインポート
from django.contrib.auth import views as auth_views  # Djangoのデフォルトログイン/ログアウトビュー
from notifications.views import mypage_notifications  # 通知のビューをインポート

urlpatterns = [
    path('', views.index, name='index'),  # トップページをindexに設定
    path('mypage/', views.mypage, name='mypage'),  # マイページへのルートを元のビューに戻す
    path('attendance/', include('attendance.urls')),  # 勤怠機能へのルート
    path('signup/', accounts_views.signup, name='signup'),  # サインアップ
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),  # ログイン
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),  # ログアウト
    path('profile/', accounts_views.edit_profile, name='edit_profile'),  # プロフィール変更
    path('activate/<uidb64>/<token>/', accounts_views.activate_account, name='activate_account'),  # アカウント認証
    path('admin/employee-list/', views.employee_list, name='employee_list'),
    path('admin/export-employees-csv/', views.export_employees_csv, name='export_employees_csv'),
    path('admin/edit-employee/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('admin/delete-employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    path('inventory/', include('inventory.urls')),
    path('customers/', include('customers.urls')),  # 顧客リストへのURL
    path('docspdf/', include('docspdf.urls')),
    path('admin/', admin.site.urls),
    path('notifications/', include('notifications.urls', namespace='notifications')),  # 通知機能を分離
    path('employee/<int:employee_id>/', views.employee_detail, name='employee_detail'),
    path("__reload__/", include("django_browser_reload.urls")),  # ここを追加
    path('accounts/', include('accounts.urls')),  # 追加
]

from django.conf import settings
from django.conf.urls.static import static

# 修正：static() を正しく適用
if settings.DEBUG:  # ローカルでのみ動作
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path("preview-error/<int:error_code>/", views.preview_error, name="preview_error"),
    ]

from django.conf.urls import handler400, handler403, handler404, handler500
from django.shortcuts import render

def error_view(request, exception=None, error_code=500, error_title="エラー", error_message="予期しないエラーが発生しました。"):
    return render(request, "error.html", {
        "error_code": error_code,
        "error_title": error_title,
        "error_message": error_message,
    }, status=error_code)

handler400 = lambda request, exception: error_view(request, exception, 400, "不正なリクエスト", "申し訳ありません。リクエストに問題があります。")
handler403 = lambda request, exception: error_view(request, exception, 403, "アクセス拒否", "申し訳ありません。このページにアクセスする権限がありません。")
handler404 = lambda request, exception: error_view(request, exception, 404, "ページが見つかりません", "申し訳ありません。お探しのページは存在しないか、移動した可能性があります。")
handler500 = lambda request: error_view(request, None, 500, "サーバーエラー", "申し訳ありません。サーバー内部で問題が発生しました。しばらくしてから再度お試しください。")
