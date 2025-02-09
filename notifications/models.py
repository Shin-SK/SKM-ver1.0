from django.db import models
from django.utils.timezone import now

class Notification(models.Model):
    # 通知のタイトル
    title = models.CharField(max_length=255)
    
    # 通知の本文
    body = models.TextField()
    
    # 通知のタイプ（全体通知または部署通知）
    NOTIFICATION_TYPES = [
        ('全体', '全体'),
        ('部署', '部署'),
    ]
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    
    # 部署名（部署通知の場合のみ指定）
    department = models.CharField(max_length=255, blank=True, null=True)
    
    # 通知作成日時
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 通知予約日時（デフォルトは現在時刻）
    scheduled_at = models.DateTimeField(default=now)
    
    # 通知が送信されたかどうか
    sent = models.BooleanField(default=False)

    def __str__(self):
        return self.title
