from django.shortcuts import render, get_object_or_404
from .models import Notification
from django.contrib.auth.decorators import login_required

@login_required
def mypage_notifications(request):
    """マイページ（最新5件のみ表示）"""
    notifications = Notification.objects.filter(notification_type='全体').order_by('-created_at')[:5]
    return render(request, 'notifications/mypage_notifications.html', {'notifications': notifications})

@login_required
def notification_list(request):
    """通知の一覧ページ（全通知を表示）"""
    notifications = Notification.objects.filter(notification_type='全体').order_by('-created_at')
    return render(request, 'notifications/notification_list.html', {'notifications': notifications})

@login_required
def notification_detail(request, notification_id):
    """通知の詳細ページ"""
    notification = get_object_or_404(Notification, id=notification_id)
    return render(request, 'notifications/notification_detail.html', {'notification': notification})
