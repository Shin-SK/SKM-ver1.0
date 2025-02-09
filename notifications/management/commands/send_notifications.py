from django.core.management.base import BaseCommand
from django.utils.timezone import now
from noti.models import Notification
from django.core.mail import send_mail

class Command(BaseCommand):
    help = "Send scheduled notifications"

    def handle(self, *args, **kwargs):
        notifications = Notification.objects.filter(scheduled_at__lte=now(), sent=False)
        for notification in notifications:
            # メール送信ロジック
            if notification.notification_type == '全体':
                recipients = ['recipient1@example.com', 'recipient2@example.com']  # 全体通知の場合の宛先
            elif notification.notification_type == '部署' and notification.department:
                recipients = ['department@example.com']  # 部署通知の場合の宛先

            send_mail(
                subject=notification.title,
                message=notification.body,
                from_email='your_email@example.com',
                recipient_list=recipients,
                fail_silently=False,
            )

            # 送信済みにマーク
            notification.sent = True
            notification.save()

        self.stdout.write(self.style.SUCCESS("Notifications sent successfully."))
