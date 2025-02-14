from django.db import models
import random

class Employee(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="名", blank=True, null=True)
    last_name = models.CharField(max_length=50, verbose_name="姓", blank=True, null=True)
    email = models.EmailField(unique=True, verbose_name="メールアドレス", blank=True, null=True)
    department = models.CharField(max_length=100, verbose_name="部署", blank=True, null=True)
    phone_number = models.CharField(max_length=15, verbose_name="電話番号", blank=True, null=True)
    employee_number = models.CharField(
        max_length=6, unique=True, blank=True, null=True, verbose_name="社員番号"
    )

    def save(self, *args, **kwargs):
        if not self.employee_number:
            while True:
                random_number = f"{random.randint(100000, 999999)}"
                if not Employee.objects.filter(employee_number=random_number).exists():
                    self.employee_number = random_number
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.employee_number or '未設定'})"


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    custom_fields = models.JSONField(default=dict, blank=True)  # カスタムフィールド

    def __str__(self):
        return self.name