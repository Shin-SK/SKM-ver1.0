from django.core.management.base import BaseCommand
from notifications.models import Notification
from django.utils.timezone import now

class Command(BaseCommand):
    help = 'スケジュールされた通知を送信します'

    def handle(self, *args, **kwargs):
        scheduled_notifications = Notification.objects.filter(
            scheduled_at__lte=now(),
            sent=False
        )
        for notification in scheduled_notifications:
            # 通知を送信（例: メールやログ出力）
            print(f"送信: {notification.title}")
            notification.sent = True
            notification.save()

        self.stdout.write(self.style.SUCCESS('通知の送信が完了しました'))
