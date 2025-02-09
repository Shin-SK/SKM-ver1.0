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
