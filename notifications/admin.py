from django.contrib import admin
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'notification_type', 'scheduled_at', 'created_at', 'sent')
    list_filter = ('notification_type', 'scheduled_at', 'created_at', 'sent')
    search_fields = ('title', 'body')
    ordering = ('-scheduled_at',)  # 予約日時の降順

    def save_model(self, request, obj, form, change):
        # モデルの保存処理のみ
        super().save_model(request, obj, form, change)

        # メール送信対象の設定
        recipients = []
        if obj.notification_type == '全体':
            recipients = ['recipient1@example.com', 'recipient2@example.com']  # 適宜変更
        elif obj.notification_type == '部署' and obj.department:
            recipients = ['department@example.com']  # 適宜変更

        # メール本文をテンプレートから作成
        email_body = render_to_string('notifications/email_notification.html', {
            'title': obj.title,
            'body': obj.body,
            'notification_type': obj.notification_type,
            'department': obj.department,
        })

        # メール送信
        email = EmailMessage(
            subject=obj.title,
            body=email_body,
            from_email='your_email@gmail.com',
            to=recipients,
        )
        email.content_subtype = "html"  # HTMLメールを指定
        email.send()

        # ターミナル出力（デバッグ用）
        # print(f"メール送信完了: {email_body}")
