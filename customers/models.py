from django.db import models
from cloudinary.models import CloudinaryField  # Cloudinaryをインポート

class Customer(models.Model):
    company_name = models.CharField(max_length=255, default="デフォルト会社名", verbose_name="会社名")
    first_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="姓")
    last_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="名")
    email = models.EmailField(unique=True, verbose_name="メールアドレス")
    phone_number = models.CharField(max_length=15, null=True, blank=True, verbose_name="電話番号")
    address = models.TextField(null=True, blank=True, verbose_name="住所")
    logo = CloudinaryField(blank=True, null=True, verbose_name="会社ロゴ")  # Cloudinary に変更！
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        verbose_name = "顧客"
        verbose_name_plural = "顧客情報"

    def __str__(self):
        return self.company_name
