from django.urls import path
from . import views

urlpatterns = [
    path('clock_in/', views.clock_in, name='clock_in'),  # 出勤
    path('clock_out/', views.clock_out, name='clock_out'),  # 退勤
    path('dashboard/', views.attendance_dashboard, name='attendance_dashboard'),  # 勤怠ダッシュボード
    path('admin_list/', views.admin_attendance_list, name='admin_attendance_list'),  # 管理者向け勤怠リスト
    path('export_csv/', views.export_attendance_csv, name='export_attendance_csv'),  # 勤怠データCSVエクスポート
    path('edit/<int:record_id>/', views.edit_attendance, name='edit_attendance'),
]
