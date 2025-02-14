from django.contrib import admin
from .models import Employee
from django.contrib.auth.models import Group, User

# ユーザー管理とグループ管理を非表示にする
admin.site.unregister(Group)
admin.site.unregister(User)

# 管理画面のカスタマイズ
admin.site.index_title = "管理者用ダッシュボード"

@admin.register(Employee)  # ← ここだけでOK！
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email', 'department', 'employee_number')
    search_fields = ('last_name', 'first_name', 'email', 'department', 'employee_number')
    list_filter = ('department',)

# メニュー名を変更
Employee._meta.verbose_name = "社員情報"
Employee._meta.verbose_name_plural = "社員情報"
