from django.db import models
from cloudinary.models import CloudinaryField  # Cloudinaryをインポート

class Customer(models.Model):
    COMPANY_CHOICES = [
        ('株式会社', '株式会社'),
        ('有限会社', '有限会社'),
        ('合同会社', '合同会社'),
        ('なし', 'なし'),
    ]
    company_name = models.CharField(
        max_length=255,
        choices=COMPANY_CHOICES,
        default='なし',
        verbose_name="会社名"
    )
    first_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="姓")
    last_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="名")
    email = models.EmailField(verbose_name="メールアドレス")  # unique=True を削除
    phone_number = models.CharField(max_length=15, null=True, blank=True, verbose_name="電話番号")
    address = models.TextField(null=True, blank=True, verbose_name="住所")
    logo = CloudinaryField(blank=True, null=True, verbose_name="会社ロゴ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        verbose_name = "顧客"
        verbose_name_plural = "顧客情報"

    def __str__(self):
        return self.company_name
