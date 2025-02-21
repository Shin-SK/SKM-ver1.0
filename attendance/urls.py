from django.urls import path
from . import views
from .views import delete_direct_start  # ← 追加！

urlpatterns = [
    path('clock_in/', views.clock_in, name='clock_in'),
    path('clock_out/', views.clock_out, name='clock_out'),
    path('dashboard/', views.attendance_dashboard, name='attendance_dashboard'),
    path('admin_list/', views.admin_attendance_list, name='admin_attendance_list'),
    path('export_csv/', views.export_attendance_csv, name='export_attendance_csv'),
    path('edit/<int:record_id>/', views.edit_attendance, name='edit_attendance'),
    path('set_attendance_status/', views.set_attendance_status, name='set_attendance_status'),  # ← 追加
    path('set_direct_start/', views.set_direct_start, name='set_direct_start'),  # 直行予約のルート
    path("delete_direct_start/<int:direct_start_id>/", delete_direct_start, name="delete_direct_start"),
]
