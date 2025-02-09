from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('mypage/', views.mypage_notifications, name='mypage'),  # マイページ（最新5件）
    path('allpost/', views.notification_list, name='allpost'),  # 一覧ページ（全通知）
    path('<int:notification_id>/', views.notification_detail, name='notification_detail'),  # 詳細ページ
]
