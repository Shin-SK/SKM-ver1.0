# attendance/models.py
from django.db import models
from django.contrib.auth.models import User

class AttendanceRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ユーザーとの関連付け
    clock_in = models.DateTimeField(null=True, blank=True)  # 出勤時間
    clock_out = models.DateTimeField(null=True, blank=True)  # 退勤時間
    date = models.DateField(auto_now_add=True)  # 勤務日

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class AttendanceStatus(models.Model):
    STATUS_CHOICES = [
        ('normal', '通常勤務'),
        ('morning_off', '午前休'),
        ('afternoon_off', '午後休'),
    ]
    record = models.OneToOneField(AttendanceRecord, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='normal')

    def __str__(self):
        return f"{self.record.user.username} - {self.record.date} - {self.get_status_display()}"

class DirectStart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    is_direct_start = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.date} - {'直行' if self.is_direct_start else '通常'}"
